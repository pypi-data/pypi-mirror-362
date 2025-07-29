from typing import List, Dict, Union, Any, Optional
from pydantic import BaseModel
from .job_types import Job, JobDetail, JobResult, JobStats
from .enums import (
    JobExecutionStatus, 
)

class BaseResponse(BaseModel):
    message: str

class PaginationResponse(BaseModel):
    page: int
    limit: int 
    total_count: int

class JobStatsResponse(BaseResponse):
    job_stats: JobStats

class JobEstimatedCostResponse(BaseResponse):
    job_estimated_cost: int

class JobCreationResponse(BaseResponse):
    job: Job

class JobExecutionResponse(BaseResponse):
    status: JobExecutionStatus
    job_result: Union[JobResult, Dict[str, Any]]

    class Config:
        json_encoders = {
            JobExecutionStatus: lambda v: v.value
        }

class GetJobResponse(BaseResponse):
    job: JobDetail

class GetJobsResponse(BaseResponse):
    jobs: List[Job]
    pagination: Optional[PaginationResponse] = None

class GetJobResultResponse(BaseResponse):
    job_result: JobResult
