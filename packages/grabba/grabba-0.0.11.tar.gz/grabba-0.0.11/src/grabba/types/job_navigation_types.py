from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field, HttpUrl
from .job_task_types import WebDataSelector
from .enums import JobNavigationType

class LinearNavigationOptions(BaseModel):
    regex_pattern: Optional[str] = None
    next_page_selector: Optional[WebDataSelector] = None

class BreadthFirstNavigationOptions(BaseModel):
    regex_pattern: Optional[str] = None
    max_links_per_page: Optional[int] = Field(10, ge=1, le=100)
    skip_parent: Optional[bool] = None

class CustomPathNavigationOptions(BaseModel):
    urls: str

class JobNavigation(BaseModel):
    type: JobNavigationType
    options: Optional[Union[LinearNavigationOptions, BreadthFirstNavigationOptions, CustomPathNavigationOptions]] = None
    max_pages: Optional[int] = Field(50, ge=1, le=1000)

    class Config:
        json_encoders = {JobNavigationType: lambda v: v.value}
