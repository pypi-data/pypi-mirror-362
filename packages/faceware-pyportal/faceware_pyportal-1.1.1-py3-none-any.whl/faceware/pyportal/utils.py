"""Utility methods."""
import re
import unicodedata
import asyncio
import aiohttp
from faceware.pyportal import exceptions

REPLACEMENT_CHARACTER_NON_ASCII = 'x'
"""
We replace non-ASCII characters in filename to their ASCII equivalents
But sometime there is no equivalent and in that case python replaces it with `?`

We will replace the `?` with `x`. This is to prevent filename with `?`.
This also helps if all the character in the filename cannot be converted to ASCII
"""


def sanitize_name(filename: str) -> str:
    """Convert to ASCII. Convert spaces or repeated dashes to single dashes.

    Remove characters that aren't alphanumerics, dot, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.
    >>> __sanitize_name('El.Niño 2023-2024.jpg')
    'el.nino_2023_2024.jpg'

    Args:
      filename: Filename of string type

    Returns:
      Sanitized filename containing only ASCII characters
    """
    value = str(filename)
    value = (unicodedata.normalize('NFKD',
                                   value).encode('ascii',
                                                 'replace').decode('ascii'))
    # encode with replace with replace all the non-ascii chars with
    # ? the official REPLACEMENT CHARACTER
    # we will replace the ? with `REPLACEMENT_CHARACTER_NON_ASCII`
    value = value.replace('?', REPLACEMENT_CHARACTER_NON_ASCII)
    value = re.sub(r'[^\w.\s-]', '', value.lower())
    value = re.sub(r'[-\s]+', '_', value).strip('-_')
    return value


def is_connection_failure(exception: BaseException) -> bool:
    """Will check if the exception is due to connection failure."""
    exception_checks = [
        'Operation timed out', 'Connection aborted.', 'bad handshake: ',
        'Failed to establish a new connection', 'Connection refused',
        'Failed to resolve', 'Cannot connect to ', 'Connection reset by peer'
    ]
    if isinstance(exception, aiohttp.ServerTimeoutError):
        return True
    for check in exception_checks:
        if check in str(exception):
            return True
    return False


def is_retryable_failure(exception: Exception) -> bool:
    """Will inspect the incoming exception if it can be retried."""
    if isinstance(exception, exceptions.PortalHTTPException):
        return exception.is_retryable
    if isinstance(exception, aiohttp.ClientConnectionError):
        return True
    if isinstance(exception, asyncio.TimeoutError):
        return True
    return False
