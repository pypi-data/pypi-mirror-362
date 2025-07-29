
This is a python library for submitting new jobs & downloading results of processed jobs from Faceware Portal.


## Installation and Prerequisites

This library requires 
- Faceware Portal Account and Access Token
- python >= 3.8

```bash
  pip install faceware-pyportal
```
    
## Usage

You can find general usage documentation at [https://docs.facewaretech.com/](https://docs.facewaretech.com).


```python
import logging
from faceware.pyportal.job import TrackingModel
from faceware.pyportal.job_result import JobStatus
from faceware.pyportal import PortalClient

# set your desired logging level
logging.basicConfig(level=logging.INFO)

client = PortalClient(
    access_token="{YOUR-ACCESS-TOKEN}",
    organization_id="{YOUR-ORGANIZATION-ID}"
    parent_logger=logging.getLogger('pyportal') # Optional
)

project = await client.get_project("{PROJECT-ID}")

job = await project.submit_job(
    actor_name="Sample"
    tracking_model=TrackingModel.STATIC_CAM,
    video_file_path="samples/Video.mp4",
    calibration_image_file_path="samples/Calibration.jpg"
)

while await job.get_status() not in [JobStatus.COMPLETED, JobStatus.FAILED]:
    print("waiting for job status to change")

if job.status is JobStatus.COMPLETED:
    await job.download_retargeting_file('samples/tracked.fwr')
```

### Support

For support, email support@facewaretech.com
