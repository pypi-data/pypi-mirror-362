from typing import Optional, Union
from pydantic import BaseModel
from datetime import datetime
from .enums import JobSchedulePolicy

class OneTimeSchedule(BaseModel):
    timezone: str
    timestamp: datetime  # Automatically converts from string to datetime

class JobSchedule(BaseModel):
    policy: JobSchedulePolicy
    specification: Optional[
        Union[OneTimeSchedule, str]
    ] = None
    last_run: Optional[datetime] = None

    class Config:
        json_encoders = {JobSchedulePolicy: lambda v: v.value}


