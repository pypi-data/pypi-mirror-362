from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from job_server.db import SessionLocal
from job_server.models import Job

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/healthz")
def health_check():
    return {"status": "ok"}

@router.get("/metrics")
def basic_metrics(db: Session = Depends(get_db)):
    return {
        "queued": db.query(Job).filter(Job.status == "queued").count(),
        "in_progress": db.query(Job).filter(Job.status == "in_progress").count(),
        "completed": db.query(Job).filter(Job.status == "completed").count(),
        "failed": db.query(Job).filter(Job.status == "failed").count(),
    }
