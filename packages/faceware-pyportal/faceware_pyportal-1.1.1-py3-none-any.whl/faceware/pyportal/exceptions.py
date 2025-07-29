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
"""List of exceptions when using API."""
import json
import aiohttp
from typing import Optional, Any

HTTP_RETRYABLE_CODES = [
    408,  # Request Timeout
    429,  # Too Many Requests
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    504  # Gateway Timeout
]

HTTP_LIMIT_EXCEEDED_MESSAGE = 'Limit Exceeded'
"""
The Rest API will reply with this string when the client has reached the API quota.
"""


class AccessTokenNotFoundError(Exception):
    """Raise error if access token not found.
     
    Error happens if access_token is not a part of client initialization and `FACEWARE_PORTAL_API_ACCESS_TOKEN` env var is not set.
    """

    def __init__(self, message):
        """Initialize the AccessTokenNotFoundError exception.

        Args:
            message: Error message to provide the context.
        """
        super().__init__(message)


class OrganizationIdNotFoundError(Exception):
    """Raise error if organization id not found.
     
    Error happens if organization is not a part of client initialization and `FACEWARE_PORTAL_ORGANIZATION_ID` env var is not set.
    """

    def __init__(self, message):
        """Initialize the OrganizationIdNotFoundError exception.

        Args:
            message: Error message to provide the context.
        """
        super().__init__(message)


class DownloadError(Exception):
    """Raise Download error based on REST API HTTPS response status code."""

    def __init__(self, message):
        """Initialize the DownloadError exception.

        Args:
            message: Error message to provide the context.
        """
        super().__init__(message)


class UploadFailureException(Exception):
    """Raise Invalid request exception based on REST API HTTPS response status code."""

    def __init__(self, message):
        """Initialize the UploadFailureException exception.

        Args:
            message: Error message to provide the context.
        """
        super().__init__(message)


class InvalidPortalResponseException(Exception):
    """Raise error if API response data can't be validated."""

    def __init__(self, message='Unexpected data format received from API'):
        """Initialize the InvalidDataException exception.
        
        Args:
            message: Error message to provide the context.
        """
        super().__init__(message)


class PortalHTTPException(Exception):
    """All Portal HTTP exceptions use this class."""

    response: aiohttp.ClientResponse
    portal_error_message: str = None
    portal_error_code: str = None
    _is_retryable: bool = False

    @property
    def is_retryable(self):
        """Return whether or not error should be retried."""
        return self._is_retryable

    def __init__(self,
                 response: aiohttp.ClientResponse,
                 response_content: Optional[Any] = None) -> None:
        """Create a new PortalHTTPException.

        Args:
            response: The response to the HTTP request
            response_content: The response content
        """
        super().__init__()
        self.response = response
        self._is_retryable = response.status in HTTP_RETRYABLE_CODES
        if response_content is not None:
            try:
                if 'message' in response_content:
                    self.portal_error_message = response_content['message']
                else:
                    self.portal_error_message = ''
                if 'portalErrorCode' in response_content:
                    self.portal_error_code = response_content['portalErrorCode']
                else:
                    self.portal_error_code = ''
                self._is_retryable &= self.portal_error_message != HTTP_LIMIT_EXCEEDED_MESSAGE
            except (json.JSONDecodeError, KeyError):
                pass

    def __str__(self) -> str:
        """Generate and return the string representation of the object.

        Returns:
            A string representation of the object
        """
        if self.portal_error_message is not None and self.portal_error_code is not None:
            return (f'<method={self.response.method}, ' +
                    f'url={self.response.url}, ' +
                    f'status_code={self.response.status}, ' +
                    f'is_retryable={self._is_retryable}, ' +
                    f'portal_error_message={self.portal_error_message}, ' +
                    f'portal_error_code={self.portal_error_code}>')

        return (f'<method={self.response.method}, ' +
                f'url={self.response.url}, ' +
                f'status_code={self.response.status}, ' +
                f'is_retryable={self._is_retryable}>')
