from pydantic import BaseModel

class JobRequest(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int
    target: str  # emulator, device, browserstack

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    message: str
