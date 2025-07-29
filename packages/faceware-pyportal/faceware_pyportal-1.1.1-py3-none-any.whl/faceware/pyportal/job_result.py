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
"""Module for Cloud Portal job results."""
from aiolimiter import AsyncLimiter
import errno
import logging
import os
import asyncio
from enum import Enum
from . import constant, exceptions
from .base_component import BaseComponent
from typing import Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, RootModel, ValidationError

JOB_STATUS_RATE_LIMIT = AsyncLimiter(1, 5)
"""
Allow maximum of 1 job status query in 5 seconds
"""

JOB_PROGRESS_RATE_LIMIT = AsyncLimiter(1, 5)
"""
Allow maximum of 1 job progress query in 5 seconds
"""


class DownloadType(Enum):
    """Result download type."""

    RETARGETING_FILE = 'fwr'
    """
    FacewareTech Retargeter download type.
    Visit: https://facewaretech.com/software/retargeter/ for more information on Retargeter.
    """

    FACEWARE_ANALYZER_PROJECT = 'fwt'
    """
    FacewareTech Analyzer download type.
    Visit: https://facewaretech.com/software/analyzer/ for more information on Retargeter.
    """

    CONTROL_DATA = 'controls'
    """
    FacewareTech Portal Controls JSON download type.
    """

    VALIDATION_VIDEO = 'validationVideo'
    """
    Tracking quality validation video download type.
    """


class GetJobStatusResponse(BaseModel):
    """Pydantic class for get job status response validation."""
    status: str
    extended_status: Optional[str] = Field(None, alias='extendedStatus')


class GetJobProgressResponse(BaseModel):
    """Pydantic class for get job progress response validation."""
    progress: float


class GetJobDownloadResponse(RootModel[Dict[DownloadType, HttpUrl]]):
    """Pydantic class for job result validation."""
    pass


class JobStatus(Enum):
    """Job status type."""

    IN_PROGRESS = 'IN_PROGRESS'
    QUEUED = 'QUEUED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'
    NOT_FOUND = 'NOT_FOUND'
    NOT_SUBMITTED = 'NOT_SUBMITTED'
    UNKNOWN = ''

    @staticmethod
    def from_str(label):
        """Convert label to JobStatus."""
        if label == 'IN_PROGRESS':
            return JobStatus.IN_PROGRESS
        elif label == 'QUEUED':
            return JobStatus.QUEUED
        elif label == 'COMPLETED':
            return JobStatus.COMPLETED
        elif label == 'FAILED':
            return JobStatus.FAILED
        elif label == 'CANCELED':
            return JobStatus.CANCELED
        elif label == 'NOT SUBMITTED':
            return JobStatus.NOT_SUBMITTED
        else:
            return JobStatus.UNKNOWN


class JobResult(BaseComponent):
    """A class encapsulating Cloud Portal job result.
    
    Not intended to be initalized directly. Will be added as a property to the submitted/processed jobs.
    """
    project_id: str
    id: str
    video_name: str
    status: JobStatus
    extended_status: str
    progress: str
    processing_seconds: float

    def __init__(self,
                 project_id: str,
                 id: str,
                 video_name: Optional[str] = None,
                 status: Optional[JobStatus] = None,
                 extended_status: Optional[str] = None,
                 progress: Optional[int] = None,
                 processing_seconds: Optional[float] = None) -> None:
        """Initialize JobResult.

        Args:
            project_id: The identifier for the project within the organization.
            id: The identifier of the job.
            video_name: The name of the video.
            status: The current job status.
            extended_status: The extended status explanation.
            progress: The current job progress.
            processing_seconds: The number of processing seconds.
        """
        self.project_id = project_id
        self.id = id
        self.video_name = video_name
        self.status = status
        self.extended_status = extended_status
        self.progress = progress
        self.processing_seconds = processing_seconds

    async def get_status(self):
        """Get current job status."""
        async with JOB_STATUS_RATE_LIMIT:
            response, response_json = await self.api.get(
                constant.get_job_status_api_url(self.project_id, self.id))
            if response.status == 404:
                self.status = JobStatus.NOT_FOUND
                return self.status
            try:
                validated_response = GetJobStatusResponse(**response_json)
            except ValidationError as e:
                self.log.error(
                    f'Response validation error while getting job status {e}')
                raise exceptions.InvalidPortalResponseException
            job_status = validated_response.status
            extended_job_status = validated_response.extended_status
            self.log.info('JobResult: Job status of %s -> %s', self.id,
                          job_status)
            self.status = JobStatus.from_str(job_status)
            self.extended_status = extended_job_status
            return self.status

    async def get_progress(self):
        """Get current job progress."""
        async with JOB_PROGRESS_RATE_LIMIT:
            response, response_json = await self.api.get(
                constant.get_job_progress_api_url(self.project_id, self.id))
            if response.status == 404:
                self.log.error('Job not found')
                return
            try:
                validated_response = GetJobProgressResponse(**response_json)
            except ValidationError as e:
                self.log.error(
                    f'Response validation error while getting job progress {e}')
                raise exceptions.InvalidPortalResponseException
            self.progress = validated_response.progress
            return self.progress

    async def download_retargeting_file(self,
                                        absolute_file_name,
                                        progress_listener=None) -> bool:
        """Download retargeting file."""
        return await self.__handle_file_download(absolute_file_name,
                                                 DownloadType.RETARGETING_FILE,
                                                 progress_listener)

    async def download_analyzer_file(self,
                                     absolute_file_name,
                                     progress_listener=None) -> bool:
        """Download analyzer file."""
        return await self.__handle_file_download(
            absolute_file_name, DownloadType.FACEWARE_ANALYZER_PROJECT,
            progress_listener)

    async def download_control_data(self,
                                    absolute_file_name,
                                    progress_listener=None) -> bool:
        """Download control data."""
        return await self.__handle_file_download(absolute_file_name,
                                                 DownloadType.CONTROL_DATA,
                                                 progress_listener)

    async def download_validation_video(self,
                                        absolute_file_name,
                                        progress_listener=None) -> bool:
        """Download validation_video."""
        return await self.__handle_file_download(absolute_file_name,
                                                 DownloadType.VALIDATION_VIDEO,
                                                 progress_listener)

    async def __handle_file_download(self,
                                     absolute_file_name,
                                     download_type: DownloadType,
                                     progress_listener=None) -> bool:
        parent_dir = os.path.dirname(absolute_file_name)
        parent_dir_exists = os.path.exists(os.path.abspath(parent_dir))
        if parent_dir_exists is not True:
            self.log.error(
                'JobResult: Trying to download a file in non-existent direcotry %s',
                parent_dir)
            raise NotADirectoryError(errno.ENOENT, os.strerror(errno.ENOENT),
                                     parent_dir)
        _, response_json = await self.api.get(
            url=constant.get_job_downloads_api_url(self.project_id, self.id),
            query_parms={'type': download_type.value})
        try:
            validated_response = GetJobDownloadResponse(**response_json)
        except ValidationError as e:
            self.log.error(
                f'Response validation error while getting result download URL {e}'
            )
            raise exceptions.InvalidPortalResponseException
        # Validated response returns httpurl type, so we have to convert to string
        url_to_download = str(validated_response.root[download_type])
        self.log.info(f'url to download {url_to_download}')
        self.log.info('JobResult: Started downloading at %s',
                      absolute_file_name)
        await self.api.download_file(absolute_file_name, url_to_download,
                                     progress_listener)
        self.log.info('JobResult: Download completed %s', absolute_file_name)
        return True
