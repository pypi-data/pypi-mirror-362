from pydantic import BaseModel
from datetime import datetime

class JobCreate(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int
    target: str

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    test_path: str
    app_version_id: str
    created_at: datetime

class JobStatusUpdate(BaseModel):
    status: str  # "completed" or "failed"
