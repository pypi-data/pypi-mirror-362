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
"""Module for Cloud Portal projects."""

from aiolimiter import AsyncLimiter
from stat import S_ISDIR, S_ISREG
from . import constant, exceptions
from typing import Optional, List, Callable
from .job import TrackingModel, VideoRotation, Job
from .job_result import JobStatus, JobResult
from .base_component import BaseComponent
from dataclasses import dataclass
from pydantic import BaseModel, Field, ValidationError

VALID_FILTERING_STATUSES = [
    JobStatus.IN_PROGRESS, JobStatus.COMPLETED, JobStatus.QUEUED,
    JobStatus.FAILED, JobStatus.CANCELED
]

JOB_SUBMISSION_RATE_LIMIT = AsyncLimiter(1, 2)
"""
Allow maximum of 1 job submission in 2 seconds
"""


@dataclass
class JobResults:
    """Data class used for .get_jobs() response."""
    jobs: List[Job]
    next: Optional[str] = None
    limit: Optional[int] = None


class PostJobResponse(BaseModel):
    """Pydantic class for post job response data validation."""
    job_id: str = Field(..., alias='jobId')


class JobResponseInput(BaseModel):
    """Pydantic class for job input data validation."""
    tracking_model: str = Field(..., alias='trackingModel')
    tracking_version: str = Field(..., alias='trackingVersion')
    rotation: int
    video_name: str = Field(..., alias='videoName')


class JobResponse(BaseModel):
    """Pydantic class for received job data validation."""
    job_id: str = Field(..., alias='jobId')
    project_id: str = Field(..., alias='projectId')
    actor_name: str = Field(..., alias='actorName')
    status: str
    extended_status: str = Field(..., alias='extendedStatus')
    progress: int
    processing_seconds: float = Field(..., alias='processingSeconds')
    input: JobResponseInput


class GetJobsResponse(BaseModel):
    """Pydantic class for get jobs response data validation."""
    results: List[JobResponse]
    limit: Optional[int] = None
    next: Optional[str] = None


class Project(BaseComponent):
    """A class encapsulating Cloud Portal Project.

    Intended to be initilized via the client, not directly.

    Has the following accessible properties:
    - name
    - description
    - logo
    - id
    - enabled
    - job_count
    - processed_seconds

    !!! warning
        The `job_count`, `enabled`, and `processed_seconds` properties are not updated in real-time and added only for filtering purposes when the projects are loaded via project `get_project` and `get_projects` methods.
    For the latest updates run these methods again.
    """
    name: str
    description: Optional[str]
    logo: Optional[str]
    id: str
    enabled: Optional[bool]
    job_count: Optional[int]
    processed_seconds: Optional[float]

    def __init__(self,
                 id: str,
                 name: str,
                 description: Optional[str],
                 logo: Optional[str] = None,
                 enabled: Optional[bool] = None,
                 job_count: Optional[int] = None,
                 processed_seconds: Optional[float] = None) -> None:
        """Initialize Project.

        Args:
            id: Unique project ID.
            name: Name of the project.
            description: Description of the project.
            logo: Base 64 encoded project logo.
            enabled: Enabled status of the project.
            job_count: Number of jobs in the project.
            processed_seconds: Total number of processed seconds.
        """
        self.id = id
        self.name = name
        self.description = description
        self.logo = logo
        self.enabled = enabled
        self.job_count = job_count
        self.processed_seconds = processed_seconds

    async def submit_jobs(
        self,
        actor_name: str,
        tracking_model: TrackingModel,
        video_files_paths: List[str],
        calibration_image_file_path: Optional[str] = None,
        video_rotation: Optional[VideoRotation] = VideoRotation.NONE,
        tracking_version: Optional[str] = None,
        upload_progress_listener: Optional[Callable[[float], None]] = None
    ) -> List[Job]:
        """Submits multiple jobs for processing video files.

        Args:
            actor_name: The name of the actor for whom the jobs are being submitted
            tracking_model: Select if the video was recorded on Head cam or static cam
            video_files_paths: A list of absolute local file system filepaths to the video files. File size limit is 5TiB.
            calibration_image_file_path: Absolute local file system filepath to the calibration image file
            video_rotation: The orientation of the camera when videos were recorded
            tracking_version: Tracking version for Jobs.
            upload_progress_listener: A callback for tracking the file upload progress. 

        upload_progress_listener example:
            ```python
            def progress_listener(progress) -> None:
                print(f"Upload progress: {progress}%")
            ```

        Raises:
            TypeError: If the project is disabled.
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.

        Returns:
            List of submitted job objects.
        """
        if not video_files_paths:
            self.log.debug('No video files provided')
            return []
        if self.enabled is False:
            raise TypeError("Can't submit jobs for disabled project")
        submitted_jobs = []
        for video_file_path in video_files_paths:
            job = await self.submit_job(actor_name, tracking_model,
                                        video_file_path,
                                        calibration_image_file_path,
                                        video_rotation, tracking_version,
                                        upload_progress_listener)
            submitted_jobs.append(job)
        return submitted_jobs

    async def submit_job(
        self,
        actor_name: str,
        tracking_model: TrackingModel,
        video_file_path: str,
        calibration_image_file_path: Optional[str] = None,
        video_rotation: Optional[VideoRotation] = VideoRotation.NONE,
        tracking_version: Optional[str] = None,
        upload_progress_listener: Optional[Callable[[float],
                                                    None]] = None) -> Job:
        """Will create new job and submit it for processing.

        Args:
            actor_name: The name of the actor for this job
            tracking_model: Select if the video was recorded on Head cam or static cam
            video_file_path: Absolute local file system filepath to the video file. File size limit is 5TiB.
            calibration_image_file_path: Absolute local file system filepath to the calibration image file
            video_rotation: The orientation of the camera when video was recorded.
            tracking_version: Tracking version for Job.
            upload_progress_listener: A callback for tracking the file upload progress. 

        upload_progress_listener example:
            ```python
            def progress_listener(progress) -> None:
                print(f"Upload progress: {progress}%")
            ```
        
        Raises:
            TypeError: If the project is disabled.
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.

        Returns:
            Job object.
        """
        async with JOB_SUBMISSION_RATE_LIMIT:
            if self.enabled is False:
                raise TypeError("Can't submit a job for a disabled project.")
            job = Job(self.id, actor_name, tracking_model, video_file_path,
                      calibration_image_file_path, video_rotation,
                      tracking_version)
            job.validate_job()
            # calibration file upload
            if job.calibration_image_file_path is not None:
                self.log.debug('Uploading the calibration image')
                job._uploaded_image_s3_key = await self.api.upload_file(
                    job.calibration_image_file_path, job.project_id)
            # video file upload
            self.log.debug('Uploading the video')
            job._uploaded_video_s3_key = await self.api.upload_file(
                job.video_file_path, job.project_id, upload_progress_listener)
            # post the job
            job_id = await self.__post_job(job)
            job._job_result = JobResult(job.project_id, job_id)
            job._job_result.status = JobStatus.IN_PROGRESS
            return job

    async def __post_job(self, job: Job) -> str:
        self.log.info('Job: Posting job for processing')
        body = {
            'actorName': job.actor_name,
            'trackingModel': job.tracking_model.value,
            'rotation': job.video_rotation.value,
            'videoKey': job._uploaded_video_s3_key,
        }
        if job.tracking_version is not None:
            body['trackingVersion'] = job.tracking_version

        if job._uploaded_image_s3_key is not None:
            body['calibrationImageKey'] = job._uploaded_image_s3_key

        _, response_json = await self.api.post(
            url=constant.get_job_post_api_url(job.project_id), body=body)
        try:
            validated_job_response = PostJobResponse(**response_json)
        except ValidationError as e:
            self.log.error(f'Response validation error while posting job {e}')
            raise exceptions.InvalidPortalResponseException
        job_id = validated_job_response.job_id
        self.log.info('Job: Posted job for processing. Job id: %s', job_id)
        return job_id

    async def get_jobs(self,
                       next: Optional[str] = None,
                       limit: Optional[int] = None,
                       status: Optional[List[JobStatus]] = None) -> JobResults:
        """Get the list of all jobs in the project.

        Args:
            next: the token use for pagination, will be returned with a previous get_jobs() request if the limit was set. Used to load next sequence of the jobs
            limit: how many jobs to load
            status: filter jobs based on the JobStatus

        Valid filtering statuses:
            - JobStatus.IN_PROGRESS
            - JobStatus.QUEUED
            - JobStatus.COMPLETED
            - JobStatus.FAILED

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.
            exceptions.InvalidPortalResponseException: If portal responded with invalid or unexpected format.
            ValueError: If the invalid filterting status provided.
        
        Returns:
            The JobResults object.
        """
        params = {}
        if next is not None:
            params['next'] = next
        if limit is not None:
            params['limit'] = limit
        if status is not None:
            invalid_statuses = [
                s for s in status if s not in VALID_FILTERING_STATUSES
            ]
            if invalid_statuses:
                raise ValueError(
                    f"Invalid filtering statuses: {', '.join(str(s) for s in invalid_statuses)}"
                )
            params['status'] = [s.value for s in status]
        _, response_json = await self.api.get(
            constant.get_all_jobs_for_project_api_url(self.id), params)
        jobs = []
        try:
            validated_response = GetJobsResponse(**response_json)
        except ValidationError as e:
            self.log.error(f'Response validation error while getting jobs {e}')
            raise exceptions.InvalidPortalResponseException
        for item in validated_response.results:
            job = Job(project_id=self.id,
                      actor_name=item.actor_name,
                      tracking_model=TrackingModel(item.input.tracking_model),
                      video_rotation=VideoRotation(item.input.rotation),
                      tracking_version=item.input.tracking_version)
            job._job_result = JobResult(
                project_id=self.id,
                id=item.job_id,
                video_name=item.input.video_name,
                status=JobStatus.from_str(item.status),
                extended_status=item.extended_status,
                progress=item.progress,
                processing_seconds=item.processing_seconds)
            jobs.append(job)
        return JobResults(jobs, validated_response.next,
                          validated_response.limit)

    async def get_job(self, job_id: str) -> Job:
        """Get a specific job by id.

        Args:
            job_id: Unique ID to load the job.
        
        Returns:
            Job object.

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.
            exceptions.InvalidPortalResponseException: If the response from the portal is invalid.
        """
        _, response_json = await self.api.get(
            constant.get_job_by_id_api_url(self.id, job_id))
        try:
            validated_response = JobResponse(**response_json)
        except ValidationError as e:
            self.log.error(f'Response validation error while getting a job {e}')
            raise exceptions.InvalidPortalResponseException
        job = Job(project_id=self.id,
                  actor_name=validated_response.actor_name,
                  tracking_model=TrackingModel(
                      validated_response.input.tracking_model),
                  tracking_version=validated_response.input.tracking_version,
                  video_rotation=validated_response.input.rotation)
        job._job_result = JobResult(
            project_id=self.id,
            id=validated_response.job_id,
            video_name=validated_response.input.video_name,
            status=JobStatus.from_str(validated_response.status),
            extended_status=validated_response.extended_status,
            progress=validated_response.progress,
            processing_seconds=validated_response.processing_seconds)
        return job

    async def edit(self,
                   project_name: Optional[str] = None,
                   project_description: Optional[str] = None,
                   is_project_enabled: Optional[bool] = None) -> bool:
        """Edit the project information.

        Args:
            project_name: New project name.
            project_description: New project description.
            is_project_enabled: Whether the project should be enabled or disabled.

        Returns:
            True if the project was successfully updated, False otherwise.

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with the FacewareTech Portal.
        """
        self.log.info('Project: sending edit event')
        body = {}
        if project_name is not None:
            body['name'] = project_name
        if project_description is not None:
            body['description'] = project_description
        if is_project_enabled is not None:
            body['isEnabled'] = is_project_enabled
        response, _ = await self.api.post(url=constant.edit_project_by_id_url(
            self.id),
                                          body=body)
        return response.status == 200

    async def delete(self) -> bool:
        """Will delete the project if it is empty.
        
        Returns:
            True if the project deletion was succesful. False, otherwise

        Raises:
            exceptions.PortalHTTPException: If there was an error while communicating with FacewareTech Portal.
        """
        response, _ = await self.api.delete(
            constant.delete_project_by_id_url(self.id))
        return response.status == 200

    def validate_project(self):
        """Validates project before uploading."""
        self.log.info('Validating project')
        # Validates name
        if not isinstance(self.name, str):
            raise TypeError('Invalid Name')
        # Validates description
        if self.description is not None:
            if not isinstance(self.description, str):
                raise TypeError('Invalid description')
        self.log.info('Project validation finished')
