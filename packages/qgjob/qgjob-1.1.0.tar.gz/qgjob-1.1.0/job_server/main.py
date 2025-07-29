from fastapi import FastAPI
from job_server.job_api import router as job_router
from job_server.agent_api import router as agent_router
from job_server.monitoring import router as monitoring_router
from job_server.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AppWright Job Orchestrator")

app.include_router(job_router)
app.include_router(agent_router)
app.include_router(monitoring_router)
