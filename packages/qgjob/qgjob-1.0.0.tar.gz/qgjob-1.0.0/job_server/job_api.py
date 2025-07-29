from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from job_server.schemas import JobCreate, JobResponse, JobStatus, JobStatusUpdate
from job_server.db import SessionLocal
from job_server.scheduler import schedule_job
from job_server.models import Job
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs", response_model=JobResponse)
def submit_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        job_id = schedule_job(db, job)
        return {"job_id": job_id, "status": "queued", "message": "Job submitted."}
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={
                "error": "Duplicate job submission blocked.",
                "reason": "A job with the same org_id, app_version_id, test_path, and target already exists in the queue or DB.",
                "suggestion": "Check the status of your existing job or modify parameters to submit a new one."
            },
        )

@router.get("/jobs/{job_id}/status", response_model=JobStatus)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job.id,
        "status": job.status,
        "test_path": job.test_path,
        "app_version_id": job.app_version_id,
        "created_at": job.created_at,
    }

@router.post("/jobs/{job_id}/status")
def update_job_status(job_id: str, update: JobStatusUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = update.status
    db.commit()
    return {"message": f"Job {job_id} updated to {update.status}"}
