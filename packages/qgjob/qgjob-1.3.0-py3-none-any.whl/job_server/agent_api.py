from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from job_server.db import SessionLocal
from job_server.job_queue import dequeue_job
from job_server.models import Job
from fastapi.responses import Response

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/agents/next-job")
def get_next_job(target: str, app_version_id: str, db: Session = Depends(get_db)):
    job = dequeue_job(target, app_version_id)
    if not job:
        return Response(status_code=204)

    db_job = db.query(Job).filter(Job.id == job["job_id"]).first()
    if db_job:
        db_job.status = "in_progress"
        db.commit()

    return job
