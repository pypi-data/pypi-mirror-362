from job_server.models import Job
import uuid
from job_server.job_queue import enqueue_job

def schedule_job(db, job_create):
    job_id = str(uuid.uuid4())

    # Persist to DB first
    job = Job(
        id=job_id,
        org_id=job_create.org_id,
        app_version_id=job_create.app_version_id,
        test_path=job_create.test_path,
        priority=job_create.priority,
        target=job_create.target,
        status="queued"
    )
    db.add(job)
    db.commit()

    # Only enqueue in Redis after DB insert succeeds
    job_data = {
        "job_id": job_id,
        "org_id": job_create.org_id,
        "app_version_id": job_create.app_version_id,
        "test_path": job_create.test_path,
        "priority": job_create.priority,
        "target": job_create.target,
    }
    enqueue_job(job_data)

    return job_id
