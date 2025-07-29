from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from job_server.db import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, index=True)
    org_id = Column(String, index=True)
    app_version_id = Column(String, index=True)
    test_path = Column(String)
    priority = Column(Integer, default=5)
    target = Column(String)
    status = Column(String, default="queued")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    __table_args__ = (
        UniqueConstraint("org_id", "app_version_id", "test_path", "target", name="uq_job_dedup"),
    )
