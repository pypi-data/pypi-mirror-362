import requests;
from typing import Dict, List;
from ..types.enums import (
    PuppetRegion, 
);
from ..types import (
    WebAgentConfig, 
    Job, JobSchedule, JobNavigation,
    JobNavigationType, JobSchedulePolicy, 
    BaseResponse, JobExecutionResponse, JobExecutionStatus,
    GetJobResponse, GetJobsResponse, GetJobResultResponse,
    JobEstimatedCostResponse, JobStatsResponse, JobCreationResponse,
    CreateKnowledgeBaseResponse, GetKnowledgeBasesResponse, GetKnowledgeBaseResponse,
    StoreContextResponse, FetchContextResponse, UpdateContextResponse, GatherContextResponse
);
from .utils import dict_to_camel_case, dict_to_snake_case

# Grabba SDK Class
class Grabba:
    def __init__(self, api_key: str, region: PuppetRegion = PuppetRegion.US.value):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.api_url = "https://api.grabba.dev/v1"
        self.default_puppet_config = WebAgentConfig(region=region)
        self.default_job_navigation = JobNavigation(type=JobNavigationType.NONE.value)
        self.default_job_schedule = JobSchedule(policy=JobSchedulePolicy.IMMEDIATELY.value)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
    
    def get_stats(self) -> JobStatsResponse:
        response = requests.get(
            f"{self.api_url}/stats",
            headers=self._get_headers(),
        )
        # Validate response
        response.raise_for_status()
        response_obj = response.json()
        return JobStatsResponse(
            message=response_obj["message"],
            job_stats=dict_to_snake_case(response_obj["jobStats"])
        )

    def estimate_job_cost(self, job: Job) -> JobEstimatedCostResponse:
        job = Job.model_validate(job)
        if not job.puppet_config:
            job.puppet_config = self.default_puppet_config
        if not job.navigation:
            job.navigation = self.default_job_navigation
        if not job.schedule:
            job.schedule = self.default_job_schedule
        job_data = job.model_dump(by_alias=True, exclude_none=True)
        # convert job object keys to camelCase
        jobToCamelCase = dict_to_camel_case(job_data)
        # Send request
        response = requests.post(
            f"{self.api_url}/estimate-job-cost",
            headers=self._get_headers(),
            json=jobToCamelCase,
        )
        # Return response for only 'BadRequest' and 'response.OK'
        if response.ok:
            response_obj = response.json()
            return JobEstimatedCostResponse(
                message=response_obj['message'], 
                job_estimated_cost=response_obj['jobEstimatedCost']
            )
        if response.status_code == 400:
            # Catch error message
            response_obj = response.json()
            job_errors = { "errors": response_obj }
            return JobExecutionResponse(
                message="BadRequestError", 
                job_estimated_cost=job_errors
            )
        return response.raise_for_status()

    def create_job(self, job: Job) -> JobExecutionResponse:
        job = Job.model_validate(job)
        # Ensure job is only created, not executed.
        job.schedule = JobSchedule(policy=JobSchedulePolicy.REMAIN_IDLE.value)
        if not job.puppet_config:
            job.puppet_config = self.default_puppet_config
        if not job.navigation:
            job.navigation = self.default_job_navigation
        job_data = job.model_dump(by_alias=True, exclude_none=True)
        # convert job object keys to camelCase
        jobToCamelCase = dict_to_camel_case(job_data)
        # Send request
        response = requests.post(
            f"{self.api_url}/create-job",
            headers=self._get_headers(),
            json=jobToCamelCase,
        )
        # Return response for only 'BadRequest' and 'response.OK'
        if response.ok:
            response_obj = response.json()
            return JobCreationResponse(
                message=response_obj['message'],
                job=dict_to_snake_case(response_obj['job'])
            )
        if response.status_code == 400:
            # Catch error message
            response_obj = response.json()
            job_errors = { "errors": response_obj }
            return JobCreationResponse(
                message="BadRequestError", 
                job=job_errors
            )
        return response.raise_for_status()
    
    def extract(self, job: Job) -> JobExecutionResponse:
        job = Job.model_validate(job)
        if not job.puppet_config:
            job.puppet_config = self.default_puppet_config
        if not job.navigation:
            job.navigation = self.default_job_navigation
        if not job.schedule:
            job.schedule = self.default_job_schedule
        job_data = job.model_dump(by_alias=True, exclude_none=True)
        # convert job object keys to camelCase
        jobToCamelCase = dict_to_camel_case(job_data)
        # Send request
        response = requests.post(
            f"{self.api_url}/extract",
            headers=self._get_headers(),
            json=jobToCamelCase,
        )
        # Return response for only 'BadRequest' and 'response.OK'
        if response.ok:
            response_obj = response.json()
            return JobExecutionResponse(
                status=response_obj['status'], 
                message=response_obj['message'], 
                job_result=dict_to_snake_case(
                    response_obj['jobResult'],
                    skip_regex=r'^\d+\s-\s.+$' # Skips task output key
                )
            )
        if response.status_code == 400:
            # Catch error message
            response_obj = response.json()
            job_errors = { "errors": response_obj }
            return JobExecutionResponse(
                status=JobExecutionStatus.ERROR,
                message="BadRequestError", 
                job_result=job_errors
            )
        return response.raise_for_status()
    
    def schedule_job(self, job_id: str) -> JobExecutionResponse:
        response = requests.post(
            f"{self.api_url}/schedule-job/{job_id}",
            headers=self._get_headers(),
        )
        # Return response for only 'BadRequest' and 'response.OK'
        if response.ok:
            response_obj = response.json()
            return JobExecutionResponse(
                status=response_obj['status'], 
                message=response_obj['message'], 
                job_result=dict_to_snake_case(
                    response_obj['jobResult'],
                    skip_regex=r'^\d+\s-\s.+$' # Skips task output key
                )
            )
        if response.status_code == 400:
            # Catch error message
            response_obj = response.json()
            job_errors = { "errors": response_obj }
            return JobExecutionResponse(
                status=JobExecutionStatus.ERROR,
                message="BadRequestError", 
                job_result=job_errors
            )
        return response.raise_for_status()

    def get_jobs(self, page=1, limit=25) -> GetJobsResponse:
        response = requests.get(
            f"{self.api_url}/jobs?page={page}&limit={limit}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        response_obj = response.json()
        return GetJobsResponse(
            message=response_obj['message'],
            jobs=dict_to_snake_case(
                response_obj['jobs'],
                skip_regex=r'^\d+\s-\s.+$'
            ),
            pagination=dict_to_snake_case(
                response_obj['pagination']
            )
        )

    def get_job(self, job_id: str) -> GetJobResponse:
        response = requests.get(
            f"{self.api_url}/jobs/{job_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        response_obj = response.json()
        return GetJobResponse(
            message=response_obj["message"],
            job=dict_to_snake_case(response_obj['job'])
        )
    
    def delete_job(self, job_id: str) -> BaseResponse:
        response = requests.delete(
            f"{self.api_url}/jobs/{job_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return BaseResponse(**response.json())

    def get_job_result(self, job_result_id: str) -> GetJobResultResponse:
        response = requests.get(
            f"{self.api_url}/job-result/{job_result_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        response_obj = response.json()
        return GetJobResultResponse(
                message=response_obj['message'], 
                job_result=dict_to_snake_case(
                    response_obj['jobResult'],
                    skip_regex=r'^\d+\s-\s.+$' # Skips task output key
                )
            )
    
    def delete_job_result(self, job_result_id: str) -> BaseResponse:
        response = requests.delete(
            f"{self.api_url}/job-result/{job_result_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return BaseResponse(**response.json())

    def get_available_regions(self) -> List[Dict[str, PuppetRegion]]:
        return [{k: v.value} for k, v in PuppetRegion.__members__.items()]

    # Knowledge Base Methods
    def create_knowledge_base(self, name: str, description: str = None) -> CreateKnowledgeBaseResponse:
        payload = {"name": name}
        if description:
            payload["description"] = description
        
        response = requests.post(
            f"{self.api_url}/knowledge-bases",
            headers=self._get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return CreateKnowledgeBaseResponse(**response.json())

    def get_knowledge_bases(self) -> GetKnowledgeBasesResponse:
        response = requests.get(
            f"{self.api_url}/knowledge-bases",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetKnowledgeBasesResponse(**response.json())

    def get_knowledge_base(self, kb_id: str) -> GetKnowledgeBaseResponse:
        response = requests.get(
            f"{self.api_url}/knowledge-bases/{kb_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetKnowledgeBaseResponse(**response.json())

    def delete_knowledge_base(self, kb_id: str) -> BaseResponse:
        response = requests.delete(
            f"{self.api_url}/knowledge-bases/{kb_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return BaseResponse(**response.json())

    def store_context(self, kb_id: str, context: str, metadata: Dict = None) -> StoreContextResponse:
        payload = {"context": context}
        if metadata:
            payload["metadata"] = metadata

        response = requests.post(
            f"{self.api_url}/knowledge-bases/{kb_id}/context",
            headers=self._get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return StoreContextResponse(**response.json())

    def fetch_context(self, kb_id: str, query: str, options: Dict = None) -> FetchContextResponse:
        payload = {"query": query}
        if options:
            payload["options"] = options

        response = requests.get(
            f"{self.api_url}/knowledge-bases/{kb_id}/context",
            headers=self._get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return FetchContextResponse(**response.json())

    def update_context(self, context_id: str, content: str = None, metadata: Dict = None) -> UpdateContextResponse:
        payload = {}
        if content:
            payload["content"] = content
        if metadata:
            payload["metadata"] = metadata

        response = requests.put(
            f"{self.api_url}/knowledge-bases/context/{context_id}",
            headers=self._get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return UpdateContextResponse(**response.json())

    def delete_context(self, context_id: str) -> BaseResponse:
        response = requests.delete(
            f"{self.api_url}/knowledge-bases/context/{context_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return BaseResponse(**response.json())

    def gather_context(self, kb_id: str) -> GatherContextResponse:
        response = requests.get(
            f"{self.api_url}/knowledge-bases/{kb_id}/gather-context",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GatherContextResponse(**response.json())
    
