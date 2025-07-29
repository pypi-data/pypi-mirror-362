# Grabba Python SDK

Grabba Python SDK provides a simple and intuitive interface for scheduling web data extraction jobs, estimating costs, retrieving job results, and managing your workflows. All SDK types are implemented as Pydantic BaseModels for full JSON compatibility and built-in validation.

---

## Installation

Install the SDK using pip:

```bash
pip install grabba
```

---

## Basic Setup

### Import the Client and Required Types

```python
from grabba import (
    Grabba, Job, JobNavigationType, JobSchedulePolicy, JobTaskType,
    KnowledgeBase, ContextResult
)
```

> **Note:** All types such as `Job`, `JobTask`, etc., are now Pydantic BaseModels. They support `.model_dump()` and `.json()` for serialization, and Enum fields are automatically converted to literal values.

### Initialize a Client Instance

```python
grabba = Grabba(api_key="your-api-key", region="US")  # Optional: Defaults to US
```

---

## Methods

### extract

`grabba.extract(job: Job) -> JobExecutionResponse`

Schedules a new web data extraction job for immediate execution.

---

### schedule\_job

`grabba.schedule_job(job_id: str) -> JobExecutionResponse`

Schedules an already-created job for execution.

---

### get\_jobs

`grabba.get_jobs(page=1, limit=25) -> GetJobsResponse`

Fetches a paginated list of your submitted jobs.

---

### get\_job

`grabba.get_job(job_id: str) -> GetJobResponse`

Fetches details of a specific job.

---

### get\_job\_result

`grabba.get_job_result(job_result_id: str) -> GetJobResultResponse`

Retrieves the result of a specific completed job.

---

### delete\_job

`grabba.delete_job(job_id: str) -> BaseResponse`

Deletes a job using its job ID.

---

### delete\_job\_result

`grabba.delete_job_result(job_result_id: str) -> BaseResponse`

Deletes a specific job result.

---

### create\_job

`grabba.create_job(job: Job) -> JobCreationResponse`

Creates a job but does **not** execute it immediately.

---

### estimate\_job\_cost

`grabba.estimate_job_cost(job: Job) -> JobEstimatedCostResponse`

Estimates the cost of running a job based on its tasks, duration, and region.

---

### get\_stats

`grabba.get_stats() -> JobStatsResponse`

Fetches job usage stats for your API key.

---

### get\_available\_regions

`grabba.get_available_regions() -> List[Dict[str, str]]`

Returns a list of available regions supported by the scraping engine.

---

## Knowledge Base Methods

### create\_knowledge\_base

`grabba.create_knowledge_base(name: str, description: str = None) -> CreateKnowledgeBaseResponse`

Creates a new knowledge base.

---

### get\_knowledge\_bases

`grabba.get_knowledge_bases() -> GetKnowledgeBasesResponse`

Retrieves a list of all your knowledge bases.

---

### get\_knowledge\_base

`grabba.get_knowledge_base(kb_id: str) -> GetKnowledgeBaseResponse`

Retrieves a specific knowledge base by its ID.

---

### delete\_knowledge\_base

`grabba.delete_knowledge_base(kb_id: str) -> BaseResponse`

Deletes a specific knowledge base by its ID.

---

### store\_context

`grabba.store_context(kb_id: str, context: str, metadata: Dict = None) -> StoreContextResponse`

Stores a new context (piece of information) into a knowledge base.

---

### fetch\_context

`grabba.fetch_context(kb_id: str, query: str, options: Dict = None) -> FetchContextResponse`

Fetches relevant context from a knowledge base based on a semantic query.

---

### update\_context

`grabba.update_context(context_id: str, content: str = None, metadata: Dict = None) -> UpdateContextResponse`

Updates a specific context entry by its ID.

---

### delete\_context

`grabba.delete_context(context_id: str) -> BaseResponse`

Deletes a specific context entry by its ID.

---

### gather\_context

`grabba.gather_context(kb_id: str) -> GatherContextResponse`

Gathers and returns all unique metadata tags and values for a given knowledge base.

---

## Error Handling

The SDK throws exceptions for:

* Invalid API keys
* BadRequest responses (400)
* Network issues
* Validation errors in input models

**Example:**

```python
try:
    response = grabba.extract(job)
    print(response.job_result)
except Exception as e:
    print("Failed to run job:", e)
```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/grabba-dev/grabba-sdk).

---

## License

MIT License. See the [LICENSE](LICENSE) file.

---

## Additional Notes

* **Pydantic Serialization:**
  All SDK models support `.json()` or `.model_dump()` for easy JSON conversion.

* **Enum Fields:**
  Enum values like `JobSchedulePolicy.IMMEDIATELY` are serialized automatically to their string literals (e.g., `"IMMEDIATELY"`).

* **Type Safety:**
  All inputs are strictly validated using Pydantic.

---

## Change Log

### Version 0.0.9 (Latest)

* **New Method - `estimate_job_cost(job: Job)`**: Estimate the cost of a job before execution.
* **New Method - `create_job(job: Job)`**: Create a job without scheduling it for execution.
* **New Method - `get_stats()`**: Get usage and job stats for your API key.
* **Improved Input Validation**: More robust Pydantic-based validation.
* **Bug Fixes & Performance Improvements**

### Version 0.0.4 - 0.0.8

* **New Method - `delete_job(job_id: str)`**
* **New Method - `delete_job_result(job_result_id: str)`**
* **New Method - `get_available_regions()`**: Retrieve supported regions.
* **Performance Optimizations**
* **Bug Fixes:** Fixed serialization issues with nested Pydantic models.

### Version 0.0.3

* **Full Pydantic Integration**
* **Enum Serialization Improvements**
* **Enhanced Error Handling**

---

Let me know if you'd like a Markdown export or to update the repo structure with examples/docs as well.
