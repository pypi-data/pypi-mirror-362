from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
from .enums import (
    JobStatus, PuppetDeviceType, PuppetRegion
)
from .job_task_types import JobTask, JobTaskOutput
from .job_schedule_types import JobSchedule
from .job_navigation_types import JobNavigation


class WebAgentConfig(BaseModel):
    region: PuppetRegion = PuppetRegion.US
    device_type: Optional[PuppetDeviceType] = None
    viewport: Optional[Dict] = None

    class Config:
        json_encoders = {
            PuppetRegion: lambda v: v.value,
            PuppetDeviceType: lambda v: v.value
        }

class JobResult(BaseModel):
    id: str
    output: Dict[str, JobTaskOutput]
    start_time: datetime
    stop_time: datetime
    duration: str

class Job(BaseModel):
    id: Optional[str] = None
    url: str
    tasks: List[JobTask]
    schedule: JobSchedule
    navigation: JobNavigation
    puppet_config: Optional[WebAgentConfig] = None

class JobDetail(BaseModel):
    id: str
    name: str
    url: str
    tasks: List[JobTask]
    schedule: JobSchedule
    navigation: JobNavigation
    puppet_config: Optional[WebAgentConfig] = None
    status: JobStatus
    results: List[JobResult] = []
    created_at: datetime

    class Config:
        json_encoders = {JobStatus: lambda v: v.value}

class JobStats(BaseModel):
    total_jobs: int
    completed_jobs: int 
    running_jobs: int
    failed_jobs: int
    token_balance: int