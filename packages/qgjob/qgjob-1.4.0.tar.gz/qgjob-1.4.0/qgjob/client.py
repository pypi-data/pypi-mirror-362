import requests
from qgjob.models import JobRequest
from qgjob.config import API_BASE_URL

def submit_job(org_id, app_version_id, test_path, priority, target):
    job = JobRequest(
        org_id=org_id,
        app_version_id=app_version_id,
        test_path=test_path,
        priority=priority,
        target=target,
    )
    try:
        resp = requests.post(f"{API_BASE_URL}/jobs", json=job.dict())
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return f"Error submitting job: {e}"

def get_status(job_id):
    try:
        resp = requests.get(f"{API_BASE_URL}/jobs/{job_id}/status")
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return f"Error checking job status: {e}"
