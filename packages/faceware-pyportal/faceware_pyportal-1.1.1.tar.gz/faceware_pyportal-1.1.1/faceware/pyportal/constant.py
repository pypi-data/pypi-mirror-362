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
"""Constants for use with the API."""
import os
from urllib.parse import urljoin, quote_plus

ENV_VAR_FACEWARE_PORTAL_API_BASE = 'FACEWARE_PORTAL_API_BASE'
""" Env var key for base url """

ENV_VAR_FACEWARE_PORTAL_API_VERSION = 'FACEWARE_PORTAL_API_VERSION'
""" Env var key for base url """

ENV_VAR_FACEWARE_PORTAL_ACCESS_TOKEN = 'FACEWARE_PORTAL_ACCESS_TOKEN'  # nosec
""" Env var key for portal access token """

ENV_VAR_FACEWARE_PORTAL_ORG_ID = 'FACEWARE_PORTAL_ORGANIZATION_ID'
""" Env var key for portal organization id """

API_VERSION = os.environ.get(ENV_VAR_FACEWARE_PORTAL_API_VERSION, 'v1')
"""
Set the api version from FACEWARE_PORTAL_API_VERSION if it exists
else use the default
"""

API_BASE_URL = os.environ.get(ENV_VAR_FACEWARE_PORTAL_API_BASE,
                              'https://api.cloud.facewaretech.com')
"""
Set the api base url from FACEWARE_PORTAL_API_BASE if it exists
else use the default
"""


def _multi_urljoin(*parts):
    return urljoin(
        parts[0],
        '/'.join(quote_plus(part.strip('/'), safe='/') for part in parts[1:]))


def get_content_upload_api_url(project_id: str, filename: str) -> str:
    """Generate content upload URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'contentuploadurl',
                          project_id, filename)


def get_all_jobs_api_url(project_id: str) -> str:
    """Generate all jobs URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs')


def get_job_status_api_url(project_id: str, jobId: str) -> str:
    """Generate job status api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs', jobId, 'status')


def get_job_progress_api_url(project_id: str, jobId: str) -> str:
    """Generate job status api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs', jobId, 'progress')


def get_job_downloads_api_url(project_id: str, jobId: str) -> str:
    """Generate job downloads api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs', jobId, 'download')


def get_job_post_api_url(project_id: str) -> str:
    """Generate job post api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs')


def get_project_post_api_url() -> str:
    """Generate project post api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects')


def get_project_by_id_url(project_id: str) -> str:
    """Generate project get api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id)


def delete_project_by_id_url(project_id: str) -> str:
    """Generate project delete api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id)


def edit_project_by_id_url(project_id: str) -> str:
    """Generate project delete api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'edit')


def get_projects_api_url() -> str:
    """Generate projects get api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects')


def get_all_jobs_for_project_api_url(project_id: str) -> str:
    """Generate all job in a project get api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs')


def get_job_by_id_api_url(project_id: str, jobId: str) -> str:
    """Generate job by id get api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs', jobId)


def get_content_upload_initialize_api_url(project_id: str,
                                          filename: str) -> str:
    """Generate content upload initialization api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'contentuploadurl',
                          project_id, filename, 'initialize')


def get_content_upload_part_api_url(project_id: str, filename: str) -> str:
    """Generate content upload part api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'contentuploadurl',
                          project_id, filename, 'parturls')


def get_content_upload_finalize_api_url(project_id: str, filename: str) -> str:
    """Generate content upload finalize api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'contentuploadurl',
                          project_id, filename, 'finalize')


def delete_job_by_id_api_url(project_id: str, jobId: str) -> str:
    """Generate job by id delete api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs', jobId)


def move_job_by_id_api_url(project_id: str, jobId: str) -> str:
    """Generate move job by id api URL."""
    return _multi_urljoin(API_BASE_URL, API_VERSION, 'projects', project_id,
                          'jobs', jobId, 'move')
