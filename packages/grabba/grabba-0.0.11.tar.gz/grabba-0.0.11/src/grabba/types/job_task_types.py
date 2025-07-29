from typing import List, Optional, Union, Any
from pydantic import BaseModel
from .enums import (
    JobTaskType,
    WebDataSelectorType, SpecificDataExtractionType,
    SpecificDataExtractionOutputFormat, WebScreenCaptureFormat, 
    StructuredDataExtractionAttribute, PdfPaperFormat, PdfOrientation
)

class WebDataSelector(BaseModel):
    type: WebDataSelectorType
    value: str

    class Config:
        json_encoders = {WebDataSelectorType: lambda v: v.value}

class StructuredDataExtractionParameter(BaseModel):
    name: str
    selector: Optional[WebDataSelector] = None
    parent_selector: Optional[WebDataSelector] = None
    attribute: Optional[StructuredDataExtractionAttribute] = None
    custom_attribute: Optional[str] = None
    sample: Optional[str] = None

    class Config:
        json_encoders = {StructuredDataExtractionAttribute: lambda v: v.value}

class StructuredDataExtractionOptions(BaseModel):
    parameters: List[StructuredDataExtractionParameter]
    auto_populate_parameters: bool = True
    parse_with_ai: bool = False
    execute_with_ai: bool = False
    parent_selector: WebDataSelector = WebDataSelector( type="css", value="body" )

class FormDataExtractionOptions(BaseModel):
    selector: Optional[WebDataSelector] = None

class TableDataExtractionOptions(BaseModel):
    selector: Optional[WebDataSelector] = None

class PresetDataExtractionOptions(BaseModel):
    selector: Optional[WebDataSelector] = None

class CustomDataExtractionOptions(BaseModel):
    regex_pattern: Optional[str] = None
    selector: Optional[WebDataSelector] = None


class SpecificDataExtractionOptions(BaseModel):
    type: SpecificDataExtractionType
    options: Union[
        PresetDataExtractionOptions, 
        TableDataExtractionOptions, 
        FormDataExtractionOptions, 
        StructuredDataExtractionOptions,
        CustomDataExtractionOptions,
        None
    ]
    max_results: int = 100
    output_format: SpecificDataExtractionOutputFormat

    class Config:
        json_encoders = {
            SpecificDataExtractionType: lambda v: v.value,
            SpecificDataExtractionOutputFormat: lambda v: v.value
        }


class WebScreenCaptureOptions(BaseModel):
    format: Optional[WebScreenCaptureFormat] = WebScreenCaptureFormat.WEBP.value
    full_page: Optional[bool] = False
    omit_background: Optional[bool] = True
    pdf_format: Optional[PdfPaperFormat] = PdfPaperFormat.A4.value
    pdf_orientation: Optional[PdfOrientation] = PdfOrientation.LANDSCAPE.value
    pdf_print_background: Optional[bool] = True

    class Config:
        json_encoders = {
            PdfOrientation: lambda v: v.value,
            PdfPaperFormat: lambda v: v.value,
            WebScreenCaptureFormat: lambda v: v.value,
        }


class WebpageAsMarkdownOptions(BaseModel):
    only_main_content: Optional[bool] = True
    apply_smart_cleaner: Optional[bool] = True


class JobTaskBase(BaseModel):
    id: Optional[str] = None
    type: JobTaskType


class JobTask(JobTaskBase):
    options: Union[
        SpecificDataExtractionOptions, 
        WebpageAsMarkdownOptions, 
        WebScreenCaptureOptions,
        None
    ]

    class Config:
        json_encoders = {JobTaskType: lambda v: v.value}


class PageOutput(BaseModel):
    source: str
    content: str


class JobTaskOutput(BaseModel):
    task: JobTaskBase
    data: List[Union[PageOutput]]
    data_url: Optional[str] = None