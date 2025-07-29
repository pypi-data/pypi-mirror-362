#############################################################################
#                                                                           #
# Copyright © 2023 Faceware Technologies, Inc.                              #
#                                                                           #
# All rights reserved.  No part of this software including any part         #
# of the coding or data forming any part thereof may be used or reproduced  #
# in any form or by any means otherwise than in accordance with any         #
# written license granted by Faceware Technologies, Inc.                    #
#                                                                           #
# Requests for permissions for use of copyright material forming            #
# part of this software (including the grant of licenses) shall be made     #
# to Faceware Technologies, Inc.                                            #
#                                                                           #
#############################################################################
"""Module for Multipart upload following chunked upload strategy."""
import logging
import aiohttp
import asyncio
import os
import io
import math
from typing import List, Optional, Dict
from os.path import basename
from pydantic import BaseModel, Field, ValidationError

from tenacity import (retry_if_exception, retry, stop_after_attempt,
                      wait_exponential_jitter, after_log)

from . import constant, exceptions
from .utils import sanitize_name, is_connection_failure, is_retryable_failure

MIN_PART_SIZE = 10 * 1024 * 1024  # 10 mb.
"""
Minimum size of each part.
"""

MAX_TOTAL_PARTS = 1000
"""
The max total part is selected at 1000 after carefully optimizing the time it takes to
finalize the large multipart uploads. Otherwise, clients would observe high latency for
finalize API call.
"""

MAX_PART_URLS_PER_REQUEST = 50
"""
Maximum batch size of part upload urls to be requested at a time
"""

PART_LIMIT_FOR_NEXT_PART_REQUEST = 20
"""
Indicates when to make the request for next batch of upload urls from
"""

API_TIMEOUT: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=16)
"""
Default timeout in seconds for each API call (initialize, finalize, hydrate).
If the API call is not completed the timeout will cancel the API call and trigger the retry
"""

MAX_UPLOAD_FILE_SIZE = 5 * math.pow(1024, 4)
"""
Max file size to upload is 5TiB.
"""


class UploadInitializeResponse(BaseModel):
    """Pydantic class for upload initialize response validation."""
    file_id: str = Field(..., alias='fileId')
    file_key: str = Field(..., alias='fileKey')


class MultiuploadPartUrl(BaseModel):
    """Pydantic class for part urls for multipart upload response validation."""
    signed_url: str = Field(..., alias='signedUrl')
    part_number: int = Field(..., alias='partNumber')


class PartUrlsForMultipartUploadResponse(BaseModel):
    """Pydantic class for part urls for multipart upload response validation."""
    parts: List[MultiuploadPartUrl]
    start_index: int = Field(..., alias='startIndex')


class MultipartUploader:
    """Class to help with managing multi part uploads. It performs chunked uploads to the server.

    Process:
        1) Initialize the upload: This will provision the backend to accept chunks for a specific file
        2) Upload chunks: This will upload the file one chunk at a time. This is done parallelly to optimize the upload time.
        3) Finalize: This will let the backend know to perform "stitch" on all the uploaded chunks.
    """
    log: logging.Logger
    _file_path: str
    _project_id: str
    _default_headers: Dict[str, str]
    _sanitized_file_name: str

    _total_parts: int
    """ Total parts of multipart the should be uploaded """

    _part_size: int
    """ Size in bytes for each part """

    _uploaded_part: [Dict[str, str]]
    """
    Array of parts that are uploaded. Each object in array is
    a dictionary with PartNumber and Etag keys.
    This will be used to finalize the multipart upload
    """

    _part_upload_urls: List[MultiuploadPartUrl]
    """
    Array of upload urls for each part. Each object has signed_url and
    part_number attributes.
    """

    _current_part_start_index: int
    """
    We only requests `MAX_PART_URLS_PER_REQUEST` part upload urls.
    This variable keeps track of which part urls should be requested
    in subsequent calls to `GET /getPreSignedUrls` API
    """

    _upload_file_id: str
    """
    Internal id issued by the backend to uniquely identify the multipart upload in progress
    """

    _upload_file_key: str
    """
    Relative location of the file on the backend storage.
    """

    _hydration_request_in_queue: bool

    _lock: asyncio.Lock

    def __init__(self,
                 file_path: str,
                 project_id: str,
                 headers: Optional[Dict] = None,
                 parent_logger: Optional[logging.Logger] = None) -> None:
        """Initialize the mulitpart uploader.
        
        Args:
            file_path: Absolute path to file on disk.
            project_id: Identifier for the project within the organization.
            headers: Optional dictonary of headers to be attached to API requests
            parent_logger: Optional logger instance.
        
        Raises:
            FileNotFoundError: If the file does not exists at specified path
        """
        if parent_logger is None:
            self.log = logging.getLogger('multipart_uploader')
        else:
            self.log = parent_logger.getChild('multipart_uploader')
            self.log.setLevel(parent_logger.level)
        if not os.path.exists(file_path):
            raise FileNotFoundError('Invalid file path')
        self._file_path = file_path
        self._project_id = project_id
        self._default_headers = headers
        self._sanitized_file_name = sanitize_name(basename(self._file_path))

        self._event_listeners = []
        self._uploaded_part = []
        self._part_upload_urls = []
        self._current_part_start_index = 0
        self._hydration_request_in_queue = False
        self._lock = asyncio.Lock()
        self._upload_file_id = None
        self._upload_file_key = None
        self._file_size = None

        self.__calculate_part_and_size()

    def __iadd__(self, listener):
        """Shortcut for using += to add a event listener.

        Will register a listener function for upload progress.
        The registered listener will receive following information:
        total parts, uploaded parts, progress in percentage
        """
        self._event_listeners.append(listener)
        return self

    def __get_client_session(self) -> aiohttp.ClientSession:
        """Will return the `aiohttp.ClientSession` with default configuration.

        Returns:
            client session with default config set
        """
        return aiohttp.ClientSession(
            raise_for_status=True,
            timeout=aiohttp.ClientTimeout(
                total=None,
                sock_read=int(os.getenv('PYPORTAL_SOCK_READ_TIMEOUT', 180))),
            headers=self._default_headers)

    def __calculate_part_and_size(self):
        """Will calculate the total parts and size of each part for the file.

        We are limiting the maximum parts to `MAX_TOTAL_PARTS` i.e. 1000. So, if the 
        parts come out to be more than `MAX_TOTAL_PARTS` based on `MIN_PART_SIZE`
        we will calculate the size for each part with maximum of `MAX_TOTAL_PARTS`.

        We are also limiting maximum file size to 'MAX_UPLOAD_FILE_SIZE'.
        
        Example 1:
        File size: 5564870785 bytes (~5.56 GB)
        Parts based on `MIN_PART_SIZE` (10 MB): 531 (Less than `MAX_TOTAL_PARTS` i.e. 1000)

        This will result in multipart upload with 531 parts with each part of size 10485760 bytes (~10 MB)

        Example 2:
        File size: 27802110785 bytes (~27.8 GB)
        Parts based on `MIN_PART_SIZE` (10 MB): 2652 (Greater than `MAX_TOTAL_PARTS` i.e. 1000)
        Calculate part size for `MAX_TOTAL_PARTS`: 27808235 bytes (~26 MB)

        This will result in multipart upload with `MAX_TOTAL_PARTS` parts with each part of size 27808235000 bytes (~26 MB)
        """
        self._file_size = os.stat(self._file_path).st_size
        if self._file_size > MAX_UPLOAD_FILE_SIZE:
            raise ValueError('File exceeds the maximum upload limit.')
        calculated_total_parts = max(-(self._file_size // -MIN_PART_SIZE), 1)
        if calculated_total_parts > MAX_TOTAL_PARTS:
            self.log.debug('Total parts: %s is higher than max allowed parts.',
                           calculated_total_parts)
            self._part_size = ((calculated_total_parts * MIN_PART_SIZE) //
                               (MAX_TOTAL_PARTS))
            self._total_parts = MAX_TOTAL_PARTS
        else:
            self._total_parts = calculated_total_parts
            self._part_size = MIN_PART_SIZE
        self.log.debug('Total parts set to: %s with each part of %s mb',
                       self._total_parts, (self._part_size // (1024 * 1024)))

    async def upload(self) -> str:
        """Will start the multipart upload to the Cloud Portal.

        Returns:
            Relative location of the file on the backend storage.
        """
        semaphore = asyncio.Semaphore(os.cpu_count() // 2)

        async with self.__get_client_session() as session:
            await self.__initialize_upload(session)
            await self.__hydrate_next_part_urls(session)
            self.__notify_progress(0)

            with open(self._file_path, mode='rb') as binary_file_reader:
                while len(self._uploaded_part) != self._total_parts:
                    tasks = []
                    # Example of calculation
                    # RS: range start
                    # RE: range end
                    # BP: Batch size for part urls that was requested
                    # TP: Total part
                    # | Iteration | RS  | RE  | BP | CP  | TP  |
                    # |-----------|-----|-----|----|-----|-----|
                    # | 0         | 0   | 50  | 50 | 50  | 152 |
                    # | 1         | 50  | 100 | 50 | 100 | 152 |
                    # | 2         | 100 | 150 | 50 | 150 | 152 |
                    # | 3         | 150 | 152 | 2  | 152 | 152 | --> break the while loop
                    # the while loop only breaks when all the parts in the file are read
                    range_start = max(
                        len(self._part_upload_urls) - MAX_PART_URLS_PER_REQUEST,
                        len(self._uploaded_part))
                    range_end = min(len(self._part_upload_urls),
                                    self._total_parts)

                    for part_index in range(range_start, range_end):
                        part_url = self._part_upload_urls[part_index].signed_url
                        part_number = self._part_upload_urls[
                            part_index].part_number
                        task = self.__upload_part(part_url, part_number,
                                                  binary_file_reader, session,
                                                  semaphore)
                        tasks.append(task)
                    self.log.debug('Added parts from %s to %s to the queue',
                                   range_start, range_end)
                    await asyncio.gather(*tasks)
                await self.__finalized_upload(session)
                return self._upload_file_key

    def __notify_progress(self, *args, **kargs):
        for listener in self._event_listeners:
            listener(*args, **kargs)

    async def __initialize_upload(self, session: aiohttp.ClientSession):

        @retry(
            retry=(retry_if_exception(is_connection_failure) |
                   retry_if_exception(is_retryable_failure)),
            after=after_log(self.log, logging.DEBUG),
            wait=wait_exponential_jitter(2, 66, 2, 5),
            stop=stop_after_attempt(5),
        )
        async def initialize_upload():
            post_url = constant.get_content_upload_initialize_api_url(
                self._project_id, self._sanitized_file_name)
            data = {
                'originalFilename': os.path.basename(self._file_path),
                'fileSize': self._file_size,
                'totalParts': self._total_parts,
            }
            async with session.request(method='POST',
                                       url=post_url,
                                       json=data,
                                       timeout=API_TIMEOUT) as response:
                if response.status != 200:
                    raise exceptions.PortalHTTPException(response=response)
                initialize_response = await response.json()
                try:
                    validated_initialize_response = UploadInitializeResponse(
                        **initialize_response)
                except ValidationError as e:
                    self.log.error(
                        f'Response validation error while initializing upload {e}'
                    )
                    raise exceptions.InvalidPortalResponseException
                self._upload_file_id = validated_initialize_response.file_id
                self._upload_file_key = validated_initialize_response.file_key
                self.log.debug(
                    'Initialized upload with file id: %s, file key: %s',
                    self._upload_file_id, self._upload_file_key)

        await initialize_upload()

    async def __finalized_upload(self, session: aiohttp.ClientSession):

        @retry(
            retry=(retry_if_exception(is_connection_failure) |
                   retry_if_exception(is_retryable_failure)),
            after=after_log(self.log, logging.DEBUG),
            wait=wait_exponential_jitter(2, 66, 2, 5),
            stop=stop_after_attempt(5),
        )
        async def finalized_upload():
            if len(self._uploaded_part) != self._total_parts:
                self.log.error(
                    'Trying to finalize upload without uploading all parts, will skip finalizing. Total part: %s, uploaded parts: %s',
                    self._total_parts, len(self._uploaded_part))
                return

            post_url = constant.get_content_upload_finalize_api_url(
                self._project_id, self._sanitized_file_name)
            finalize = {
                'fileId': self._upload_file_id,
                'fileKey': self._upload_file_key,
                'parts': self._uploaded_part,
            }
            async with session.request(method='POST',
                                       url=post_url,
                                       json=finalize,
                                       timeout=API_TIMEOUT) as response:
                if response.status != 200:
                    raise exceptions.PortalHTTPException(response=response)
                self.log.debug('Finalized upload successfully')

        await finalized_upload()

    async def __hydrate_next_part_urls(self, session: aiohttp.ClientSession):

        @retry(
            retry=(retry_if_exception(is_connection_failure) |
                   retry_if_exception(is_retryable_failure)),
            after=after_log(self.log, logging.DEBUG),
            wait=wait_exponential_jitter(2, 66, 2, 5),
            stop=stop_after_attempt(5),
        )
        async def hydrate_next_part_urls():
            async with self._lock:
                if self._hydration_request_in_queue is True:
                    self.log.error(
                        'Trying to hydrate when there is already request in queue.'
                    )
                    return
                self._hydration_request_in_queue = True
            try:
                if self._upload_file_id is None or self._upload_file_key is None:
                    raise TypeError(
                        'Need to initialize the multipart upload before getting part urls'
                    )
                parts_to_request = MAX_PART_URLS_PER_REQUEST

                if self._current_part_start_index + MAX_PART_URLS_PER_REQUEST > self._total_parts:
                    parts_to_request = max(
                        0, self._total_parts - self._current_part_start_index)
                if parts_to_request == 0:
                    self.log.debug('No more part urls to request')
                    return
                self.log.debug(
                    'Will hydrate part urls. Current size: %s, requested: %s, start index: %s',
                    len(self._part_upload_urls), parts_to_request,
                    self._current_part_start_index)
                post_url = constant.get_content_upload_part_api_url(
                    self._project_id, self._sanitized_file_name)
                dataInput = {
                    'fileId': self._upload_file_id,
                    'fileKey': self._upload_file_key,
                    'parts': parts_to_request,
                    'startIndex': self._current_part_start_index,
                }
                async with session.request(method='POST',
                                           url=post_url,
                                           json=dataInput,
                                           timeout=API_TIMEOUT) as response:
                    if response.status != 200:
                        raise exceptions.PortalHTTPException(response=response)
                    part_urls = await response.json()
                    try:
                        validated_part_urls = PartUrlsForMultipartUploadResponse(
                            **part_urls)
                    except ValidationError as e:
                        self.log.error(
                            f'Response validation error while getting parts urls {e}'
                        )
                        raise exceptions.InvalidPortalResponseException
                    self._current_part_start_index = MAX_PART_URLS_PER_REQUEST + validated_part_urls.start_index
                    async with self._lock:
                        self._part_upload_urls += validated_part_urls.parts
                    self.log.debug(
                        'Did hydrate part urls. Current size: %s, new start index: %s',
                        len(self._part_upload_urls),
                        self._current_part_start_index)
            finally:
                async with self._lock:
                    self._hydration_request_in_queue = False

        await hydrate_next_part_urls()

    async def __upload_part(self, url: str, part_number: int,
                            file: io.BufferedReader,
                            session: aiohttp.ClientSession,
                            semaphore: asyncio.Semaphore):

        @retry(
            retry=(retry_if_exception(is_connection_failure) |
                   retry_if_exception(is_retryable_failure)),
            after=after_log(self.log, logging.DEBUG),
            wait=wait_exponential_jitter(2, 66, 2, 5),
            stop=stop_after_attempt(5),
        )
        async def upload_part():
            async with semaphore:
                start_pos = (part_number - 1) * self._part_size
                file.seek(start_pos)
                data = file.read(self._part_size)

                try:
                    async with session.put(url, data=data) as response:
                        if response.status != 200:
                            raise exceptions.PortalHTTPException(
                                response=response)
                        else:
                            self.log.debug('Uploaded part %s successfully',
                                           part_number)
                            etag = response.headers.get('ETag')
                            uploaded_part = {
                                'PartNumber': part_number,
                                'ETag': etag.replace('"', ''),
                            }
                            self._uploaded_part.append(uploaded_part)
                            self.__notify_progress(100 * float(
                                len(self._uploaded_part) /
                                float(self._total_parts)))
                            if part_number >= (
                                    len(self._part_upload_urls) -
                                    PART_LIMIT_FOR_NEXT_PART_REQUEST):
                                await self.__hydrate_next_part_urls(session)
                except aiohttp.ClientOSError as e:
                    if 121 in e.args:  # WinError 121
                        self.log.warning(
                            f'Network appears unstable (WinError 121) during upload of part {part_number}'
                        )
                    else:
                        self.log.warning(
                            f'ClientOSError during upload of part {part_number}: {repr(e)}'
                        )
                    raise

        await upload_part()
