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
"""Module for Cloud Portal jobs."""

import asyncio
from enum import Enum
from . import constant, utils
from .job_result import JobResult, JobStatus
from typing import Optional, Callable
from .base_component import BaseComponent
import os


class VideoRotation(Enum):
    """Rotation angle to be applied while processing the video.

    This is useful when video that needs processing was
    captured in non-standard orientation
    """

    NONE = 0
    """ No rotation """

    ROTATE_90 = 90
    """ 90 degree clockwise """

    ROTATE_180 = 180
    """ 180 degree clockwise """

    ROTATE_270 = 270
    """ 270 degree clockwise """


class TrackingModel(Enum):
    """Tracking models."""

    STATIC_CAM = 'StaticCam'
    """
    The STATIC_CAM tracker is designed for use with stationary cameras. The actor's face can take up a
    varying amount of the total frame and can move around. Due to its flexibility as a tracker, it can be
    used with virtually any facial footage.
    """

    HEAD_CAM = 'HeadCam'
    """
    The HEAD_CAM tracker is designed to be used specifically with color videos from a head mounted camera.
    To work properly, the video must be in a vertical orientation (more tall than wide) and the face should
    be occupying the vast majority of the frame like in the example below.

    !!! tip
        Due to the stringent requirements for this tracker, if you are getting errors or an inconsistent track
        with either Headcam tracker, try using the STATIC_CAM instead to improve your chances of getting a good
        result
    """

    HEAD_CAM_GRAYSCALE = 'HeadCamGrey'
    """
    This tracker is almost identical to the HEAD_CAM tracker except for being specifically made for greyscale
    (black and white) videos and should only be used for that type of footage.

    !!! warning
        This tracking model is currently in an experimental evaluation phase.
    """


class Job(BaseComponent):
    """A class encapsulating submittable and retriable Cloud Portal Job.

    Intended to be initialized via the project, not directly.
    To submit a job for processing, use the `Project.submit_job()` method.

    Has the following accessible properties:
        - project_id
        - actor_name
        - tracking_model
        - tracking_version
        - video_name
        - video_rotation
        - status
        - progress
        - processing_seconds
        - extended_status

    !!! warning
        The `status`, `progress`, `processing_seconds` and `extended_status` properties are **not** updated in real-time and added only for filtering purposes when the jobs are loaded via project `get_job` and `get_jobs` methods.
        For the latest status and progress changes use the following methods:

        - get_status(), it will also update .status and .extended_status property; returns last status only
        - get_progress(), it will also update .progress property; returns last progress in percentage

    !!! warning
        The `video_name` property is available **only** when the jobs are loaded via `get_job` and `get_jobs` methods. Otherwise, `video_file_path` can be used.
    """
    project_id: str
    actor_name: str
    tracking_model: TrackingModel
    video_file_path: str
    video_rotation: Optional[VideoRotation] = VideoRotation.NONE
    calibration_image_file_path: Optional[str] = None
    tracking_version: Optional[str] = None

    _job_result: JobResult
    _uploaded_video_s3_key: str = None
    _uploaded_image_s3_key: str = None

    def __init__(self,
                 project_id: str,
                 actor_name: str,
                 tracking_model: TrackingModel,
                 video_file_path: Optional[str] = None,
                 calibration_image_file_path: Optional[str] = None,
                 video_rotation: Optional[VideoRotation] = VideoRotation.NONE,
                 tracking_version: Optional[str] = None) -> None:
        """Initialize Job.

        Args:
            project_id: Identifier for the project within the organization.
            actor_name: Name of the actor.
            tracking_model: The model to be used for video tracking.
            video_file_path: Path to the video file to be processed.
            calibration_image_file_path: Optional path to calibration image.
            video_rotation: Specifies the rotaation. Default is 'NONE'.
            tracking_version: Optional tracking version. Default is 'None'.
        """
        self.project_id = project_id
        self.actor_name = actor_name
        self.tracking_version = tracking_version
        self.tracking_model = tracking_model
        self.video_rotation = video_rotation
        self.video_file_path = video_file_path
        self.calibration_image_file_path = calibration_image_file_path
        self.actor_name = actor_name

        self._job_result = None
        self._uploaded_video_s3_key = None
        self._uploaded_image_s3_key = None

    @property
    def id(self):
        """Returns job ID if any.
        
        Will be `None` if the job was not submitted yet.
        """
        if self._job_result is None:
            return None
        return self._job_result.id

    @property
    def status(self):
        """Returns job status.
        
        Will return `JobStatus.NOT_SUBMITTED` if the job was not submitted yet.
        """
        if self._job_result is None:
            return JobStatus.NOT_SUBMITTED
        return self._job_result.status

    @property
    def extended_status(self):
        """Returns job extended status if any."""
        if self._job_result is None:
            return None
        return self._job_result.extended_status

    @property
    def processing_seconds(self):
        """Returns job processing seconds if any.
        
        Will be `None` if the job was not submitted yet.
        """
        if self._job_result is None:
            return None
        return self._job_result.processing_seconds

    @property
    def progress(self):
        """Returns job progress if any.
        
        Will be `None` if the job was not submitted yet.
        """
        if self._job_result is None:
            return None
        return self._job_result.progress

    @property
    def video_name(self):
        """Returns video name if any.
        
        Will be `None` if the job was not submitted yet.
        """
        if self._job_result is None:
            return None
        return self._job_result.video_name

    def validate_job(self):
        """Helper method to validate job attributes before posting for processing."""
        self.log.info('Job validation started')
        if not isinstance(self.video_rotation, VideoRotation):
            raise TypeError('Invalid Video Rotation')
        self.rotation = str(self.video_rotation.value)
        if not isinstance(self.tracking_model, TrackingModel):
            raise TypeError('Invalid TrackingModel')
        if not isinstance(self.actor_name, str):
            raise TypeError('actor_name should be str')
        if not os.path.exists(self.video_file_path):
            raise TypeError('Invalid video file path')
        if self.calibration_image_file_path is not None:
            if not os.path.exists(self.calibration_image_file_path):
                raise TypeError('Invalid calibration image file path')
        if self.tracking_version is not None and not isinstance(
                self.tracking_version, str):
            raise TypeError('tracking_version should be String')
        if self.tracking_version is not None and self.tracking_version.strip(
        ) == '':
            raise ValueError(
                'tracking_version should not contain only whitespaces')
        if not self.actor_name.split():
            raise ValueError('actor_name should not contain only whitespaces')
        self.log.info('Job validation finished')

    async def get_status(self) -> JobStatus:
        """Get current status.

        Running `get_status()` will also refresh `status` and `extended_status` (if any) properties

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.

        Usage Example:
            ```python
                while True:
                    status = await job.get_status()
                    if status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                        break
                    logging.info("Waiting for job status to change...")
            ```

        Returns:
            JobStatus.
        """
        if self._job_result is None:
            return JobStatus.NOT_SUBMITTED
        return await self._job_result.get_status()

    async def get_progress(self) -> Optional[int]:
        """Get current job processing progress.

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.

        Usage Example:
            ```python
                while True:
                    progress = await job.get_progress()
                    logging.info(f"Progress: {progress}%")
                    await asyncio.sleep(5)  # Wait before checking again
            ```

        Returns:
            A progress for submitted or completed jobs. None otherwise.
        """
        if self._job_result is None:
            return None
        return await self._job_result.get_progress()

    async def download_retargeting_file(
            self,
            absolute_file_name: str,
            progress_listener: Optional[Callable[[float],
                                                 None]] = None) -> bool:
        """Will download the Faceware Retargeter.

        For more information, visit: [Faceware Retargeter](https://facewaretech.com/software/retargeter/)

        Args:
            absolute_file_name: The location on the local filesystem where retargeting file will be downloaded.
            progress_listener: A callback to track the download progress.

        progress_listener example:
            ```python
            def progress_listener(progress) -> None:
                print(f"Upload progress: {progress}%")
            ```

        Returns:
            True if download was successful. False otherwise.
        
        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with Faceware Portal.
            exceptions.DownloadError: If there was an error while downloading with Faceware Portal.
            exceptions.FileNotFoundError: If the parent directory path to the absolute_file_name does not exists on filesystem. 
        """
        return await self._job_result.download_retargeting_file(
            absolute_file_name, progress_listener)

    async def download_analyzer_file(
            self,
            absolute_file_name: str,
            progress_listener: Optional[Callable[[float],
                                                 None]] = None) -> bool:
        """Will download the Faceware Analyzer.

        For more information, visit: [Faceware Analyzer](https://facewaretech.com/software/analyzer/)

        Args:
            absolute_file_name: The location on the local filesystem where Analyzer file will be downloaded.
            progress_listener: A callback to track the download progress.

        progress_listener example:
            ```python
            def progress_listener(progress) -> None:
                print(f"Upload progress: {progress}%")
            ```

        Returns:
            True if download was successful. False otherwise.

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with Faceware Portal.
            exceptions.DownloadError: If there was an error while downloading with Faceware Portal.
            exceptions.FileNotFoundError: If the parent directory path to the absolute_file_name does not exists on filesystem.
        """
        return await self._job_result.download_analyzer_file(
            absolute_file_name, progress_listener)

    async def download_control_data(
            self,
            absolute_file_name: str,
            progress_listener: Optional[Callable[[float],
                                                 None]] = None) -> bool:
        """Will download the FacewareTech Portal Controls JSON file.

        Args:
            absolute_file_name: The location on the local filesystem where JSON file will be downloaded.
            progress_listener: A callback to track the download progress.

        progress_listener example:
            ```python
            def progress_listener(progress) -> None:
                print(f"Upload progress: {progress}%")
            ```

        Returns:
            True if download was successful. False otherwise.

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.
            exceptions.DownloadError: If there was an error while downloading with FacewareTech Portal.
            exceptions.FileNotFoundError: If the parent directory path to the absolute_file_name does not exists on filesystem.
        """
        return await self._job_result.download_control_data(
            absolute_file_name, progress_listener)

    async def download_validaton_video(self,
                                       absolute_file_name,
                                       progress_listener=None) -> bool:
        """Will download the Faceware Portal tracking quality validation video file.

        Args:
            absolute_file_name: The location on the local filesystem where JSON file will be downloaded.
            progress_listener: A callback to track the download progress.

        progress_listener example:
            ```python
            def progress_listener(progress) -> None:
                print(f"Upload progress: {progress}%")
            ```

        Returns:
            True if download was successful. False otherwise.

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with Faceware Portal.
            exceptions.DownloadError: If there was an error while downloading with Faceware Portal.
            exceptions.FileNotFoundError: If the parent directory path to the absolute_file_name does not exists on filesystem.
        """
        return await self._job_result.download_validation_video(
            absolute_file_name, progress_listener)

    async def delete(self) -> bool:
        """Will delete the job if the job status is either completed, failed, canceled or in queue.

        Returns:
            True if the job deletion was successful. False, otherwise
        
        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with Faceware Portal.
        """
        deletable_status = [
            JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.QUEUED,
            JobStatus.CANCELED
        ]

        async def inner_delete():
            response, _ = await self.api.delete(
                constant.delete_job_by_id_api_url(self.project_id, self.id))
            return response.status == 200

        if self.status in deletable_status:
            return await inner_delete()

        self.log.debug('Querying for latest status')
        if await self.get_status() in deletable_status:
            return await inner_delete()
        self.log.warn('Cannot delete a job in %s status', self.status)
        return False

    async def move(self, target_project_id: str) -> bool:
        """Will move the job to another project if the job status is completed, failed or canceled.

        Args:
            target_project_id: The ID of the target (destination) project
        
        Returns:
            True if the job moved successfully. False, otherwise

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.
        """
        movable_status = [
            JobStatus.CANCELED, JobStatus.FAILED, JobStatus.COMPLETED
        ]

        async def inner_move():
            response, _ = await self.api.post(
                constant.move_job_by_id_api_url(self.project_id, self.id),
                {'targetProject': target_project_id})
            return response.status == 200

        if self.status in movable_status:
            return await inner_move()
        if await self.get_status() in movable_status:
            return await inner_move()
        self.log.warn('Cannot move a job in %s status', self.status)
        return False
