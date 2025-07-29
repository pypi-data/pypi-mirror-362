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
"""Module for making API requests to the Cloud Portal."""

import logging
import platform
import ssl
import pkg_resources
import aiohttp
import json

from tenacity import (retry_if_exception, retry, stop_after_attempt,
                      wait_exponential_jitter, after_log)
from typing import Optional, Dict
from . import exceptions
from .multipart_uploader import MultipartUploader
from .utils import is_connection_failure, is_retryable_failure

FILE_DOWNLOAD_SESSION_TIMEOUT: aiohttp.ClientTimeout = aiohttp.ClientTimeout(
    total=0,
    # limit chunk waiting to ensure that the client session will fail if there's no internet connection
    sock_read=60)
"""
For file downloads do not set a predefined timeout as the download time can vary a lot
based on the file size and network speed.
"""


class ApiRequests:
    """ApiRequests is a general purpose class used for making API requests.

    This class will structure requests according to the backend expectations and also supports 
    automated retries if possible.
    """

    log: logging.Logger
    default_headers: Dict

    def __init__(self, parent_logger: logging.Logger, access_token: str,
                 organization_id: str) -> None:
        """Initialize the ApiRequests class.

        Args:
            parent_logger: Logger object to be used by this class.
            access_token: Token to authenticate API requests.
            organization_id: Unique identifier for the organization.
        """
        if parent_logger is None:
            self.log = logging.getLogger('api_requests')
        else:
            self.log = parent_logger.getChild('api_requests')
            self.log.setLevel(parent_logger.level)
        ssl_version = ssl.OPENSSL_VERSION
        library_version = pkg_resources.get_distribution(
            'faceware-pyportal').version
        library_details = f'os {platform.platform()}; aiohttp {aiohttp.__version__}; python {platform.python_version()}; {ssl_version}'
        user_agent = f'FacewarePortal/FacewarePortal-Python-SDK {library_version} ({library_details})'

        self.default_headers = {
            'x-fti-api-key': access_token,
            'x-fti-org-id': organization_id,
            'Accept': 'application/json',
            'User-Agent': user_agent
        }

        self.trace_config = aiohttp.TraceConfig()
        self.trace_config.on_request_start.append(self.on_request_start)
        self.trace_config.on_response_chunk_received.append(
            self.on_response_chunk_received)
        self.trace_config.on_request_end.append(self.on_request_end)

    async def on_request_start(self, session, trace_config_ctx, params):
        """Asynchronous callback method triggered when request starts.

        This method is a part of the `aiohttp` client tracing system. It is called
        when a new client request is initiated and can be used to perform custom
        actions or logging before the request is sent.
        """
        method = params.method
        url = str(params.url)
        headers = {}
        body = {}
        trace_request_ctx = getattr(trace_config_ctx, 'trace_request_ctx', None)
        if trace_request_ctx is not None:
            headers = trace_request_ctx.get('headers')
            body = trace_request_ctx.get('body')
        formatted_headers = json.dumps(headers, indent=2, sort_keys=True)
        formatted_body = json.dumps(body, indent=2,
                                    sort_keys=True) if body else 'None'

        message = (f'Starting {method} request\n'
                   f'URL: {url}\n'
                   f'Headers:\n{formatted_headers}\n'
                   f'Body:\n{formatted_body}')
        self.log.debug(message)

    async def on_response_chunk_received(self, session, trace_config_ctx,
                                         params):
        """Asynchronous callback method triggered when response chunk received.

        This method is a part of the `aiohttp` client tracing system. It is called
        when a response received after request is submitted.
        """
        try:
            body_str = params.chunk.decode('utf-8')
            body_obj = json.loads(body_str)
            formatted_body = json.dumps(body_obj, indent=2, sort_keys=True)
        except json.JSONDecodeError:
            # If it's not JSON, or not valid JSON, just use the original string
            formatted_body = body_str
        message = f'Received response:\n- body:\n{formatted_body}'
        self.log.debug(message)

    async def on_request_end(self, session, trace_config_ctx, params):
        """Asynchronous callback method triggered when request ended.

        This method is a part of the `aiohttp` client tracing system. It is called when
        a request ended.
        """
        message = (f'Request finished:\n'
                   f'  - Status code: {params.response.status}\n'
                   f'  - Reason: {params.response.reason}')
        self.log.debug(message)

    async def on_request_exception(self, session, context, params):
        """Asynchronous callback method triggered when exception raised.

        This method is a part of the `aiohttp` client tracing system. It is called when
        a request failed with exception.
        """
        exception_info = {'message': str(params['exception'])}
        pretty_exception_info = json.dumps(exception_info, indent=2)
        self.log.debug(f'Request Exception: {pretty_exception_info}')

    async def post(
        self,
        url: str,
        body: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> aiohttp.ClientResponse:
        """Sends a POST request.
        
        Will auto retry the in case of network related failure or
        if the request failed with retryable HTTP status code.
        Retry are done with expotential backoff. Maximum attemps: 5

        :param url: URL
        :param body: (optional) Dictionary, body to be included in the POST
        :param headers: (optional) Dictionary, additional headers to be included in the POST
        """

        @retry(
            retry=(retry_if_exception(is_connection_failure) |
                   retry_if_exception(is_retryable_failure)),
            after=after_log(self.log, logging.DEBUG),
            wait=wait_exponential_jitter(2, 66, 2, 5),
            stop=stop_after_attempt(5),
        )
        async def post() -> aiohttp.ClientResponse:
            merged_headers = self.default_headers.copy()
            if headers is not None:
                merged_headers.update(headers)
            async with aiohttp.ClientSession(
                    trace_configs=[self.trace_config]) as client_session:
                trace_request_ctx = {'headers': merged_headers, 'body': body}
                try:
                    async with client_session.request(
                            method='POST',
                            url=url,
                            json=body,
                            headers=merged_headers,
                            trace_request_ctx=trace_request_ctx) as response:
                        response_content = await response.json()
                        if response.status != 200:
                            raise exceptions.PortalHTTPException(
                                response, response_content)
                        return response, response_content
                except Exception as e:
                    await self.on_request_exception(client_session, {},
                                                    {'exception': e})
                    raise

        return await post()

    async def get(
        self,
        url: str,
        query_parms: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> aiohttp.ClientResponse:
        """Sends a GET request.
        
        Will auto retry the in case of network related failure or
        if the request failed with retryable HTTP status code
        Retry are done with expotential backoff. Maximum attemps: 5

        :param url: URL
        :param query_parms: (optional) Dictionary, query params to be included in the GET
        :param headers: (optional) Dictionary, additional headers to be included in the GET
        """

        @retry(retry=(retry_if_exception(is_connection_failure) |
                      retry_if_exception(is_retryable_failure)),
               after=after_log(self.log, logging.DEBUG),
               wait=wait_exponential_jitter(2, 66, 2, 5),
               stop=stop_after_attempt(5))
        async def get():
            merged_headers = self.default_headers.copy()
            if headers is not None:
                merged_headers.update(headers)
            async with aiohttp.ClientSession(
                    trace_configs=[self.trace_config]) as client_session:
                trace_request_ctx = {'headers': merged_headers}
                try:
                    async with client_session.request(
                            method='GET',
                            url=url,
                            params=query_parms,
                            headers=merged_headers,
                            trace_request_ctx=trace_request_ctx) as response:
                        response_content = await response.json()
                        if response.status != 200:
                            raise exceptions.PortalHTTPException(
                                response, response_content)
                        return response, response_content
                except Exception as e:
                    await self.on_request_exception(client_session, {},
                                                    {'exception': e})
                    raise

        return await get()

    async def delete(
        self,
        url: str,
        query_parms: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> aiohttp.ClientResponse:
        """Sends a DELETE request.
        
        Will auto retry the in case of network related failure or
        if the request failed with retryable HTTP status code
        Retry are done with expotential backoff. Maximum attemps: 5

        :param url: URL
        :param query_parms: (optional) Dictionary, query params to be included in the DELETE
        :param headers: (optional) Dictionary, additional headers to be included in the DELETE
        """

        @retry(retry=(retry_if_exception(is_connection_failure) |
                      retry_if_exception(is_retryable_failure)),
               after=after_log(self.log, logging.DEBUG),
               wait=wait_exponential_jitter(2, 66, 2, 5),
               stop=stop_after_attempt(5))
        async def delete():
            merged_headers = self.default_headers.copy()
            if headers is not None:
                merged_headers.update(headers)
            async with aiohttp.ClientSession(
                    trace_configs=[self.trace_config]) as client_session:
                trace_request_ctx = {'headers': merged_headers}
                try:
                    async with client_session.request(
                            method='DELETE',
                            url=url,
                            params=query_parms,
                            headers=merged_headers,
                            trace_request_ctx=trace_request_ctx) as response:
                        response_content = await response.json()
                        if response.status != 200:
                            raise exceptions.PortalHTTPException(
                                response, response_content)
                        return response, response_content
                except Exception as e:
                    await self.on_request_exception(client_session, {},
                                                    {'exception': e})
                    raise

        return await delete()

    # TODO: Figure out correct signature or way so that we are not leaking project id
    async def upload_file(self,
                          file_to_upload: str,
                          project_id: str,
                          upload_progress_listener=None) -> str:
        """Will start the multipart upload to the Cloud Portal.

        Returns:
            Relative location of the file on the backend storage.
        """
        multipart_uploader = MultipartUploader(file_to_upload, project_id,
                                               self.default_headers, self.log)
        if upload_progress_listener:
            multipart_uploader += upload_progress_listener
        return await multipart_uploader.upload()

    async def download_file(self, file_name, url, progress_listener=None):
        """Will start downloading file from the Cloud Portal.
        
        Returns:
            True if the download is successful.

        Args:
            file_name: Name for a file to be saved.
            url: The URL to download the file from.
            progress_listener: Optional callback function that takes a single 
                argument, the percentage of the download completed (0-100).
        """

        @retry(
            retry=(retry_if_exception(is_connection_failure)),
            after=after_log(self.log, logging.DEBUG),
            wait=wait_exponential_jitter(2, 66, 2, 5),
            stop=stop_after_attempt(5),
        )
        async def download_file():
            try:
                async with aiohttp.ClientSession(
                        timeout=FILE_DOWNLOAD_SESSION_TIMEOUT,
                        trace_configs=[self.trace_config]) as client_session:
                    trace_request_ctx = {'headers': self.default_headers}
                    async with client_session.request(
                            method='GET',
                            url=url,
                            headers=self.default_headers,
                            trace_request_ctx=trace_request_ctx) as r:
                        total_size = int(r.headers.get('Content-Length', 0))
                        downloaded_size = 0
                        r.raise_for_status()
                        with open(file_name, 'wb') as f:
                            async for chunk in r.content.iter_chunked(8192):
                                f.write(chunk)
                                downloaded_size += len(
                                    chunk)  # Update downloaded size
                                # Calculate and call the progress callback
                                if progress_listener and total_size > 0:
                                    progress = (downloaded_size /
                                                total_size) * 100
                                    progress_listener(progress)
                        return True
            except aiohttp.ClientResponseError as error:
                self.log.error('API: Download file failed with error: %s',
                               error)
                raise exceptions.DownloadError(
                    f'Failed to download the file. Error: {error}') from error
            except Exception as e:
                await self.on_request_exception(client_session, {},
                                                {'exception': e})
                raise

        return await download_file()
