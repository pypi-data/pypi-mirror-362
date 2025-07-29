#!/usr/bin/env python3
####################################################
# mirror_to_s3
# by Dale Magee
# BSD 3-clause License
####################################################

# stdlib imports
import sys, os, tomllib, re, asyncio
from pathlib import Path
import logging
from datetime import datetime,timedelta, timezone
from enum import Enum
from urllib3.util import parse_url
from fnmatch import fnmatchcase

# package imports
from urllib3.util import Retry
import aiofiles
import aioboto3
import botocore.exceptions
import yaml
import httpx
import httpx_retries
from httpx_retries import Retry, RetryTransport
from httpx import AsyncHTTPTransport, AsyncClient
from lxml import html
from dotenv import load_dotenv

load_dotenv()

##############
# global vars, so we don't have to pass them around everywhere
# these tend to be populated in run()

# global bucket name (string)
bucket_name = None

# global httpx client
session = None

# number of concurrent downloads allowed
MAX_DOWNLOADS = int(os.environ.get("MAX_DOWNLOADS",10))
# global semaphore to enforce MAX_DOWNLOADS
semaphore = asyncio.Semaphore(MAX_DOWNLOADS)

# dict of files which are already in the bucket when we begin
bucket_files = {}

# used for user agent (and potentially as an anonymous FTP password)
CONTACT_EMAIL = None

# nothing will actually be mirrored if this is true
DRY_RUN = False

##############
# constants

ONE_MEG = 1024**2

##############
# helper functions

def to_bool(val:str) -> bool:
	if isinstance(val,bool): return val
	return re.match(r'(True|Yes|1)',str(val),re.I) is not None

def friendly_size(size:float) -> str:
	"""
	turns a number of bytes into a hunam-readable string, e.g 42.666 MB
	"""
	size=float(size)
	names = ["bytes","KB","MB","GB","TB","PB","EB","ZB","YB"]
	
	suffix = names.pop(0)
	
	while size >= 1024:
		size /= 1024
		suffix = names.pop(0)
		if len(names) == 0: break
	
	if size % 1 == 0:
		# whole number, no decimal
		return f"{int(size)} {suffix}"
	
	if size > 1024:
		# for large numbers, make it an int, to prevent scientific notation kicking in
		# if you get here, the suffix is yottabytes. I'm impressed!
		return f"{int(size)} {suffix}"
	
	return f"{size:.4g} {suffix}"

##############
# set up logging

use_json_log = to_bool(os.environ.get("JSON_LOG",False))

suppressed_loggers = [
	"mangum", "asyncio", "boto", "boto3","s3transfer", "botocore", 
	"aiobotocore","aioboto3", "urllib3", "httpcore", "httpx",
	"httpx_retries",
]


class LogLevel(Enum):
	"""
	supported log levels, map from name to logging value
	"""
	VERBOSE = logging.DEBUG - 1 # custom level, even less important than debug
	DEBUG = logging.DEBUG
	INFO = logging.INFO
	WARN = logging.WARN

# remove silly deprecation notice
logging.Logger.warn = logging.Logger.warning

# add .verbose  log level
logging.addLevelName(LogLevel.VERBOSE.value, "VERBOSE")

def _verboselog(self,message, *args,**kwargs):
	"""
	A more verbose logging level
	"""
	if self.isEnabledFor(LogLevel.VERBOSE.value):
		self._log(LogLevel.VERBOSE.value,message, args, **kwargs)

logging.Logger.verbose = _verboselog

# choose log level from env var
desired_level = os.environ.get("LOG_LEVEL","INFO")
if desired_level in LogLevel.__members__:
	log_level = LogLevel.__members__[desired_level]
else:
	# trash input, revert to default
	log_level = LogLevel.INFO
	
# format for log messages
# (was: "[%(asctime)s] %(levelname)-4.4s [%(name)s] %(message)s" 
logging.basicConfig(level=log_level.value, format="[%(asctime)s] %(levelname)-4.4s %(message)s", datefmt='%H:%M:%S')
logger = logging.getLogger(os.path.basename(__file__))

if use_json_log:
	# jsonlog setup
	try:
		from jsonlog.utils import configure_logging # jsonlog is optional
		configure_logging(level=log_level.value,suppressed_loggers=suppressed_loggers)
	except ImportError:
		pass
else:
	# regular logging
	for log in suppressed_loggers:
		logging.getLogger(log).setLevel(logging.WARN)
		

###
# improved httpx-retries logging

async def _retry_operation_async(
	self,
	request: httpx.Request,
	send_method: callable,
) -> httpx.Response:
	"""
	This is a replacement for httpx_retries.transport.RetryTransport._retry_operation_async with improved logging.
	We monkeypatch it into httpx_retries to get better logging of retries.
	Note that this uses our logger, not the httpx-retries logger, so this "Retrying" message will not come from httpx-retries
	"""
	
	retry = self.retry
	response = None

	while True:
		if response is not None:
			retry = retry.increment()
			logger.warn(f"** Retrying ({retry.attempts_made}/{retry.total}) '{request.url}' ({response})")
			await retry.asleep(response)
		try:
			response = await send_method(request)
		except httpx.HTTPError as e:
			if retry.is_exhausted() or not retry.is_retryable_exception(e):
				raise
			
			msg = str(e)
			if msg: msg = ": " + msg
			
			response = f"{e.__class__.__name__}{msg}"
			
			continue

		if retry.is_exhausted() or not retry.is_retryable_status_code(response.status_code):
			return response

httpx_retries.transport.RetryTransport._retry_operation_async = _retry_operation_async


###############
# optional imports
try:
	import ftputil
except ImportError as ex:
	#logger.debug('ftputil not available, cannot mirror ftp sources')
	pass

###############

def get_project_info() -> dict:
	"""
	parse and return project information from pyproject.toml
	"""
	with open((Path(__file__).parent / "pyproject.toml").resolve(), "rb") as f:
		toml = tomllib.load(f)

	return toml["project"]

# grab project info and set user agent
project_info = get_project_info()

PROJECT_NAME = project_info.get('name','mirror_to_s3')
VERSION=project_info.get('version','0.0.0-dev')

logger.info(f"{PROJECT_NAME} v{VERSION}")
logger.info(f"Log Level: {LogLevel(log_level).name}")

def get_sources() -> dict:
	"""
	Locates and and parses sources.yaml, returning parsed data
	"""
	
	# (try to) locate a sources file
	file_path = os.environ.get('SOURCES_FILE',None)
	if file_path is None:
		archiver_path = Path(__file__).parent
		try_locs = { Path(".").resolve(), archiver_path, archiver_path.parent }
		found=False
		for search_dir in try_locs:
			file_path = search_dir.resolve() / "sources.yaml"
			#logger.verbose(f"Trying '{file_path}'")
			if file_path.exists():
				found=True
				break
				
		if not found:
			raise ValueError(f"No sources.yaml file found! Place one in the appropriate directory or specify a SOURCES_FILE env var")
	else: 
		file_path = Path(file_path)
		if not file_path.exists():
			raise ValueError(f"Cannot read sources file, {file_path} does not exist")
		
	# file located, load it
	logger.info(f"Loading sources from '{file_path}'")
	with open(file_path.resolve(), "r") as f:
		inf = yaml.safe_load(f)
		
	return inf


def get_s3_client():
	"""
	Returns a boto3 S3 client, honouring the S3_ENDPOINT env var (so you can e.g point at a not-aws service)
	"""
	
	params = {
		"service_name": "s3",
	}
	if (endpoint := os.environ.get('S3_ENDPOINT')) is not None:
		params["endpoint_url"] = endpoint
	
	sess = aioboto3.Session()
	s3 = sess.client(**params)
	return s3
	

async def list_bucket_files(bucket:str = None) -> dict:
	"""
	get a COMPLETE list of all the files in the bucket, hitting AWS once for every thousand files (because aws is shit)
	you can either populate the bucket_name global, or specify a bucket name (which overrides the global)
	returns a dict indexed by the s3 key, each item is a dict containing file info
	"""
	
	global bucket_files
	
	if bucket is None:
		if bucket_name is None: raise ValueError("list_bucket_files with no args needs bucket_name to be set first")
		bucket = bucket_name
		
	ret = {}
	
	params = {
		'Bucket': bucket,
		'MaxKeys': 100000, # can we get more than 1000 out of aws? It seems not >:(
	}
	
	start_time = datetime.now()
	
	resp = None
	nreqs = 0
	
	async with get_s3_client() as s3:
	
		while resp is None or resp.get('IsTruncated'):
			nreqs += 1
			if nreqs > 1:
				logger.verbose(f"Listing bucket files ({nreqs} requests and {len(ret)} files so far)...")
			else:
				logger.debug(f"Listing bucket files...")
			
			resp = await s3.list_objects_v2(**params)
			
			for obj in resp.get('Contents', []):
				ret[obj['Key']] = obj
				
			if resp.get('IsTruncated'):
				if token := resp.get('NextContinuationToken'):
					params['ContinuationToken'] = token
				else:
					raise RuntimeError(f"Bad response from S3: IsTruncated is true but we have no NextContinuationToken. S3 response: {resp}")
		
		logger.info(f"Listed {len(ret)} files in bucket ({nreqs} requests, took {datetime.now() - start_time}).")
		
		bucket_files = ret
	
	return ret
	

def bucket_file_exists(filename:str) -> bool:
	"""
	returns a bool indicating whether a given filename (key) exists in the s3 bucket
	call list_bucket_files first.
	"""
	return filename in bucket_files


async def parse_http_index(url,include=None,exclude=None,base_url=None,recursive=True) -> list:
	"""
	Given a URL for an 'index of <dir>' directory listing page,
	 retrieves the index, parses it, and spits out a list of directories and files it links to
	
	include and exclude are lists of globs to include or exclude in the result
	
	base_url is the url we started at if we're recursing. If provided, all links returned will be made relative to this.
	
	you can prevent recursing into subdirectories by specifying recursive=False if you want to do your own thing
	
	returns a list of URLs which are relative to either base_url or URL.
	"""
	
	#TODO: we might consider refactoring this function to be a generator, yielding links one by one 
	# rather than returning a huge list. however that's a little bit tricky with recursion
	
	if not url.endswith("/"):
		url += "/"
		
	if base_url is not None and not base_url.endswith("/"):
		base_url += "/"
	
	if include is None: include = []
	if exclude is None: exclude = []
	
	async with semaphore:
	
		logger.info(f"Parsing index '{url}'...") # this should maybe be a .debug
		
		try:
			resp = await session.get(url)
			resp.raise_for_status()
		except Exception as ex:
			logger.error(f"Could not fetch index at '{url}' - {ex.__class__.__name__}: {ex}")
			raise ex
		
		content_type = resp.headers.get('Content-Type','text/html')
		
		if not content_type.startswith('text/html'):
			# not a HTML response... error? Download?
			raise ValueError(f"Cannot parse index, response from '{source['index_url']}' has content_type '{content_type}', not 'text/html'")
			
		
		#TODO: maybe we should spit the dummy if the text doesn't include "Index of"?
		
		parsed_url = parse_url(url)
		
		parsed_base = parsed_url
		if base_url is not None:
			parsed_base = parse_url(base_url)
		
		# parse the HTML and find hyperlinks
		tree = html.fromstring(resp.text)
		
		tasks = []
		errors=[]
		links = []
		for a in tree.xpath('//a'):
			link = a.get('href')
			text = a.text_content().strip()
			
			if link.startswith("?"):
				# links starting with ? are equerystring links - these are links for changing sort order, and we should ignore them
				#logger.verbose(f"Ignoring link to '{link}' ('{text}')")
				continue
			
			if link.startswith("/"):
				# normalise links which are relative to the host into absolute URLs
				# e.g if url was scheme://host:port/path/
				# then /path/to/file -> scheme://host:port/path/to/file
				link = parsed_url.scheme + "://" + parsed_url.netloc + link
			
			if url in link:
				# normalise absolute URLs which include the provided url (i.e relative to url)
				# into relative URLS,
				# e.g if url was scheme://host:port/path/
				# then scheme://host:port/path/to/file becomes to/file
				link = link.replace(url,"")
				
			# now that we've done the above normalisations, all links will either include a scheme, 
			#  or be relative to the provided url, so if the link specifies a scheme, then it's pointing at
			#  either a different host, or a directory on the host which is not a subdir of our url
			#  and we should ignore it
			parsed_link = parse_url(link)
			if parsed_link.scheme is not None:
				#logger.verbose(f"Ignoring link to '{link}' ('{text}') - not a subdir of '{url}'")
				continue
				
			
			# the absolute link, relative to the host
			abs_link = parsed_url.path + link
			
			# relative link, relative to the base URL (or url if that wasn't provided)
			#  this is our return value, and also what we match globs against
			rel_link = link
			if base_url is not None:
				rel_link = abs_link
				if rel_link.startswith(parsed_base.path):
					rel_link = rel_link[len(parsed_base.path):]
			
			if len(include) > 0:
				match=False
				for glob in include:
					if fnmatchcase(rel_link,glob):
						match=True
						break
				
				if not match:
					logger.verbose(f"Skipping link '{rel_link}', does not match any include rules")
					continue
			
			match=False
			for glob in exclude:
				if fnmatchcase(rel_link,glob):
					match=True
					break
					
			if match:
				logger.verbose(f"Skipping link '{rel_link}', matches an exclude rule")
				continue
			
			if recursive and link.endswith("/"): # note that this assumes that all links to directories will end with a slash. Seems to be true?
				if base_url is None: base_url = url
				tasks.append(asyncio.create_task(
					parse_http_index(url=url + link,include=include,exclude=exclude,base_url=base_url,recursive=True)
				))
			else:
				# when recursing, we don't include links to subdirectories in our result
				# but we DO return them if not recursing
				
				links.append(rel_link)
				
	if ntasks := len(tasks):
		#logger.verbose(f"Awaiting {ntasks} tasks ({url})")
	
		#for result in await asyncio.gather(*tasks):
		#	links += result
		
		done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
		for task in done:
			if task.exception() is None:
				_links, _errors = task.result()
				links += _links
				errors += _errors
			else:
				errors.append(task.exception())
		
	return links, errors

async def mirror_http_file(url,s3_key,msg_prefix="") -> tuple:
	"""
	Fetch a file via HTTP and upload it into s3
	returns a tuple with (bytes_downloaded:int, error:None|str)
	
	msg_prefix is text to prepend to the "Retrieving file" log message
	"""
	error=None
	filebytes=0
	
	async with (semaphore, 
				aiofiles.tempfile.NamedTemporaryFile() as f, 
				get_s3_client() as s3, 
				session.stream("GET",url) as resp
	):
		file_start = datetime.now()
	
		if msg_prefix and not msg_prefix.endswith(" "):
			msg_prefix += " "
			
		#logger.verbose(f"{msg_prefix}Retrieving '{url}' -> '{s3_key}'...")
		
		try:
			#resp = await session.get(url)
			resp.raise_for_status()
			
			# download file into a temporary file
			async for chunk in resp.aiter_bytes(ONE_MEG):
				# TODO: this iterator can throw an exception (ReadTimeout being the most common).
				#  if it does, httpx-retries doesn't handle it. It might be necessary to implement
				#  our own retry logic. Maybe cleaner too.
				if chunk:
					filebytes += len(chunk)
					await f.write(chunk)
			
		except Exception as ex:
			msg = f"Could not retrieve '{url}': {ex.__class__.__name__} - {ex}"
			#logger.error(msg,exc_info=ex)
			logger.error(msg,exc_info=ex)
			return (0, msg)
		
		# file retrieved OK, upload to S3:
		try:
			#TODO: This could use a multipart upload to do the file in chunks as we iterate over response content
			await f.seek(0) # reset pointer to start of file
			await s3.upload_fileobj(f, bucket_name, s3_key)
			
		except Exception as ex:
			msg = f"Could not upload '{url}': {ex.__class__.__name__} - {ex}"
			#logger.error(msg,exc_info=ex)
			logger.error(msg,exc_info=ex)
			return (0, msg)
			
		elapsed = datetime.now() - file_start
		rate = filebytes / elapsed.total_seconds()
		logger.info(f"{msg_prefix}'{s3_key}' OK, {friendly_size(filebytes)} in {elapsed}, {friendly_size(rate)}/sec")
	
	return (filebytes, error)

############################
# Handlers for processing sources based on URI schema
#  these must:
#	* be async
#	* be named process_xxx_source, where xxx is the URI scheme
#	* return a (downloaded_files:int, downbytes:int, already_exists:int, errors: list[str]) tuple

async def process_http_source(source) -> tuple:
	"""
	Mirror an HTTP(s) source.
	Note the process_https_source alias below - this handles both http 
		and https sources, and you need to account for that
		
	"""
	# list of error messages
	errors = []
	
	index_start = datetime.now()
	try:
		links, errors = await parse_http_index(
			url=source['index_url'],
			include=source['include'],
			exclude=source['exclude'],
			recursive=True
		)
	except Exception as ex:
		msg = f"Error processing index for source '{source['name']}': {ex.__class__.__name__} - {ex}"
		logger.error(msg,exc_info=ex)
		return (0, 0, 0, [msg])
	
	if len(errors)>0:
		for err in errors:
			logger.error(f"Error enumerating index: {err.__class__.__name__} - {err}",exc_info=err)
	
	# number of files downloaded
	downloaded_files = 0
	# number of files skipped because they already exist
	#  (other files may be skipped for other reasons, but those are not returned by parse_http_index)
	already_exists = 0
	
	# total bytes downloaded
	downbytes = 0
	
	# links processed
	processed = 0
	# number of links found
	nlinks = len(links)
	
	logger.info(f"Found {nlinks} files at source in {datetime.now() - index_start}, {len(errors)} errors")
	
	# mysterious
	start_time = datetime.now()
	
	# list of awaitables
	tasks = []
	
	# number of tasks that are queued concurrently
	MAX_QUEUE_SIZE=MAX_DOWNLOADS * 3
	
	# milestone for progress reporting
	last_milestone=0
	
	for link in links:
		processed += 1
		
		
		fn = link.lstrip("/")
		dest_dir = source['dest_dir'].rstrip("/")
		dest = f"{dest_dir}/{fn}"
		
		fetch=False
		# check if matches any globs in the refresh list
		for glob in source['refresh']:
			if fnmatchcase(link,glob):
				fetch=True
				#logger.verbose(f"'{link}' matches refresh rule '{glob}'")
				break
		
		if not fetch: # if it's in the refresh list we don't need to check whether it exists
			fetch = (not bucket_file_exists(dest))
			#if not fetch:
			#    logger.verbose(f"Skipping {dest}, file exists in bucket")
		
		if not fetch:
			# we skipped this file because it already exists
			already_exists += 1
		else:
			# retrieve the file
			
			url = source['index_url'] + link
			
			msg_prefix = f"({processed}/{nlinks})"
			filebytes = 0
			
			if DRY_RUN:
				logger.debug(f"{msg_prefix} (dry run) Mirror '{url}' -> '{dest}'")
				
			else:
				
				tasks.append(asyncio.create_task(
					mirror_http_file(url,dest,msg_prefix)
				))
				
				if len(tasks) >= MAX_QUEUE_SIZE:
					done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
					tasks = list(pending)
					for task in done:
						filebytes, error = task.result()
						
						if error is not None:
							errors.append(error)
						
						downbytes += filebytes
						downloaded_files += 1
						
						if downloaded_files - last_milestone >= 100:
							logger.debug(f"{downloaded_files} files done so far, {friendly_size(downbytes)} in {datetime.now() - start_time}")
							last_milestone = downloaded_files
					
	
	# all tasks queued, process the remaining queue as tasks finish:
	for result in asyncio.as_completed(tasks):
		
		filebytes, error = await result
		
		if error is not None:
			errors.append(error)
		
		downbytes += filebytes
		downloaded_files += 1
		
		
	elapsed = datetime.now() - start_time
	logger.info(f"Source '{source['name']}' complete in {elapsed}: {len(links)} files at source, {already_exists} already exist, {downloaded_files} files mirrored ({friendly_size(downbytes)})")
	
	return (downloaded_files, downbytes, already_exists, errors)

######
# aliases to allow processing HTTPS sources with the HTTP functions
process_https_source = process_http_source 
mirror_https_file = mirror_http_file

####

async def process_ftp_source(source) -> tuple:
	"""
	Mirror an FTP source.
	Abandoned for the time being, the FTP source I was looking at (ftp://mussel.srl.caltech.edu/pub/ace/level2) 
	 was quite slow, slower than http.
	"""
	
	raise NotImplementedError("FTP sources are currently not supported, more work is needed on process_ftp_source. Implement that, or use a http(s) source")
	
	"""
	#WIP support for FTP
	#TODO(?) we could add support for ftp + tls using ftplib.FTP_TLS
	
	parsed = source['parsed_url']
	
	logger.info(f"Connecting to FTP host '{parsed.host}'")
	
	# default to anonymous and maintainer email if no creds provided in the source
	username = source.get('username','anonymous')
	password = source.get('password',CONTACT_EMAIL)
	
	with ftputil.FTPHost(parsed.host,username,password) as ftp:
		
		for path,dirs,files in ftp.walk(parsed.path):
			print("PATH",path, " has ", len(dirs), " subdirs and ", len(files), " files")
	
	return True
	"""


############

def ensure_valid_globlist(source,key):
	"""
	Ensures that the specified key in the provided dict:
	 - exists
	 - is a list
	 - contains only strings that are >0 length
	 
	Note that this modifies source in place, returning nothing
	"""
	
	# ensure key exists
	if key not in source:
		source[key] = []
		
	# ensure it's a list
	if type(source[key]) is not list:
		source[key] = [source[key]]
	
	# filter out shit
	source[key] = [i for i in source[key] if type(i) is str and len(i) > 0]
	

async def process_source(source) -> tuple:
	"""
	Process one source from sources.yaml, mirroring files into our S3 bucket
	
	Returns a tuple containing: (downloaded_files, downbytes, already_exists, errors)
		0	number of files downloaded
		1	number of bytes downloaded
		2	number of files not downloaded because they already exist
		3	list of error messages
	(this is the required return value from the process_xxx_source functions)
	
	This is the master dispatcher which:
	1. does some validation to ensure the source is valid
	2. figures out the appropriate scheme (ftp, http) based on the source's index_url
	3. dispatches the request to the appropriate process_xxx_source method
	4. returns the result from that
	
	process_xxx_source functions can assume that:
	- the provided source is valid (i.e has all the required_fields)
	- the source has a dest_dir value, either provided by the source or calculated here based on the name
	
	"""
	
	required_fields = ['name']
	for f in required_fields:
		if f not in source:
			raise ValueError(f"Source is missing required '{f}' field")
	
	# you can set enabled=false(ish) to have the archiver ignore a source.
	enabled = to_bool(source.get("enabled",True))
	if not enabled:
		logger.warn(f"Skipping disabled source '{source['name']}'")
		return (0, 0, 0, [])
	
	url = source.get('index_url',source.get('file_url'))
	logger.info(f"Processing source '{source['name']}' ({url})")
	
	# you must have either an index_url or a file_url field
	# index_url: an 'index of' page with links to other directories/files to mirror
	# file_url: to mirror a single file
	index_url = source.get('index_url')
	file_url = source.get('file_url')
	if index_url is None and file_url is None:
		raise ValueError(f"Source '{source.get('name')}' must have either an index_url or a file_url field")
	
	# you must not have both file and index URLs
	if index_url is not None and file_url is not None:
		raise ValueError(f"Source '{source.get('name')}' must only have one of index_url / file_url fields")
	
	# if no dest_dir is specified in the source, determine one based on the name
	dest_dir = source.get('dest_dir')
	if dest_dir is None or str(dest_dir.strip()) == '':
		 # strip leading/trailing spaces
		dest_dir = source['name'].strip()
		dest_dir = re.sub(r"\s+","_",dest_dir) # space -> underscore, nuke multiple spaces
		dest_dir = re.sub(r"[^\w]","",dest_dir) # remove nonalpha characters
		logger.verbose(f"Calculated dest_dir for source: {dest_dir}")
		
	# dest_dir can include {DATE}, to download the same URLs each day into a different destination directory
	# Note that this uses UTC time
	for itm, replacement in { 
		'DATE': datetime.now(timezone.utc).strftime("%Y_%m_%d"),
		# we could add a DATETIME entry here if we wanted to run more than daily
	}.items():
		dest_dir = dest_dir.replace("{"+itm+"}",replacement)
	
	source['dest_dir'] = dest_dir
	
	# normalise lists
	for key in ['include','exclude','refresh']: 
		ensure_valid_globlist(source,key)    
	
	if file_url:
		# file_url source, mirror a single file:
		
		#source_start = datetime.now()
		
		parsed = parse_url(file_url)
		
		# we use the same mirror_xxx_file function as used by process_xxx_source to fetch files and mirrot them into S3
		fn_name = f"mirror_{parsed.scheme}_file"
		fn = globals().get(fn_name)
		if fn is None:
			raise ValueError(f"No handler available for '{parsed.scheme}' URLs! Implement a '{fn_name}' method or change the index URL for source '{source['name']}'")
			
		# note that we don't check whether the file exists for file_url sources, refreshing is the default behaviour
		dest_filename = dest_dir.rstrip("/") + "/" + os.path.basename(parsed.path)
		
		# fetch the file
		bytes_downloaded, error = await fn(file_url,dest_filename)
		
		errors = [error] if error else []
		
		#elapsed = datetime.now() - source_start
		#logger.info(f"File Source '{source['name']}' complete in {elapsed}: {friendly_size(bytes_downloaded)} fetched.")
		
		# ( downloaded_files, downloaded_bytes, already_exist, errors )
		return (1, bytes_downloaded, 0, errors)
	
	elif index_url:
		# index_url source, mirror an index:
		
		parsed = parse_url(source['index_url'])
		source['parsed_url'] = parsed # add the parsed object into the source dict, so it can be reused in processing funcs
		
		fn_name = f'process_{parsed.scheme}_source'
		fn = globals().get(fn_name)
		if fn is None:
			raise ValueError(f"No handler available for '{parsed.scheme}' URLs! Implement a '{fn_name}' method or change the index URL for source '{source['name']}'")
			
		return await fn(source)
	

async def main() -> int:
	"""
	Main coroutine.
	returns an integer exit code (0 for success)
	"""
	start_time = datetime.now()
	
	global bucket_name, bucket_files, CONTACT_EMAIL, DRY_RUN, session
	
	##############
	# load env vars into settings

	required_env_vars = ['AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY','S3_BUCKET']

	if not all([os.environ.get(k) for k in required_env_vars]):
			raise ValueError("Missing environment variables - you must set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and S3_BUCKET")
	
	# you must provide EITHER a custom user agent, or a contact email
	CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", None)
	USER_AGENT = os.environ.get("USER_AGENT",None)
	if not USER_AGENT:
		if not CONTACT_EMAIL:
			raise ValueError("You must provide either a CONTACT_EMAIL or USER_AGENT env var")
		USER_AGENT = f"{PROJECT_NAME} v{VERSION}."
		
	if CONTACT_EMAIL:
		USER_AGENT += f" Contact: {CONTACT_EMAIL}"
		
	for itm in [ "VERSION","PROJECT_NAME" ]:
		# you can use certain vars in your USER_AGENT string in a mannen similar to python f-strings,
		#  i.e {VERSION}
		find = "{" + itm + "}"
		replacement = globals().get(itm,"")
		USER_AGENT = USER_AGENT.replace(find,replacement)
	
	bucket_name = os.environ.get('S3_BUCKET') 
	logger.info(f"Using S3 bucket: '{bucket_name}'")
	
	DRY_RUN = to_bool(os.environ.get('DRY_RUN',False))
	if DRY_RUN:
		logger.warn("*** This is a dry run ***")
	
	##############
	# load sources
	sources = get_sources()
	logger.info(f"Loaded {len(sources)} sources")
	
	
	##############
	# init things
	
	# set default user agent for requests
	httpx._client.USER_AGENT = USER_AGENT
	logger.debug(f"User Agent: '{httpx._client.USER_AGENT}'")
	
	# create our global httpx client
	# automatically retry requests a few times if there's an error
	NUM_RETRIES=5
	session = AsyncClient(timeout=60,transport=RetryTransport(
		transport=AsyncHTTPTransport(retries=NUM_RETRIES),
		retry=Retry(total=NUM_RETRIES, backoff_factor=1)
	))
	
	# list all files in the bucket - more efficient than checking each file individually
	await list_bucket_files()
	
	##############
	# do the thing
	
	total_files_down = 0
	total_bytes_down = 0
	total_already_existing = 0
	errors = []
	
	for source in sources:
		#TODO: We could potentially turn this into a task rather than awaiting here, processing multiple sources concurrently.
		# this would be a good way to download more faster without overloading our source hosts.
		# it would probably be wise to use one httpx client per source if we go that route, and maybe change MAX_DOWNLOADS 
		#  to be per-source rather than global.
		# A simpler alternative to this strategy would be to separate sources into multiple sources.yaml files and run the 
		#  program multiple times concurrently.
		
		if source.get('name',None) == "BREAK":
			# hack: you can add a source named "BREAK" to tell the archiver to not process any other sources
			logger.warn("Encountered a source named 'BREAK', stopping.")
			break
			
		(downloaded_files, downbytes, already_exists, source_errors) = await process_source(source)
		total_files_down += downloaded_files
		total_bytes_down += downbytes
		total_already_existing += already_exists
		errors += source_errors
	
	elapsed = datetime.now() - start_time
	success_msg = "successfully" if len(errors) == 0 else "with errors"
	logger.info(f"Completed {success_msg} in {elapsed}. Total: {total_files_down} files / {friendly_size(total_bytes_down)} downloaded, {total_already_existing} already archived, {len(errors)} errors")
	
	if len(errors) > 0:
		logger.warn(f"{len(errors)} nonfatal errors occurred:")
		for msg in errors:
			logger.warn(msg)
	
	await session.aclose()
	
	return 0 if len(errors) == 0 else 42

def run():
	"""
	Entry Point
	"""
	sys.exit(asyncio.run(main()))

if __name__ == "__main__": run()
