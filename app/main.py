from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

from agent.local_planner import LocalDeploymentPlanner


app = FastAPI(
    title="AegisOps AI",
    description="AI-powered cloud deployment and self-healing platform",
    version="1.0.0",
)


class DeploymentRequest(BaseModel):
    request: str


planner = LocalDeploymentPlanner()


@app.get("/")
def root():
    return {
        "project": "AegisOps AI",
        "message": "AI Cloud Automation Platform is running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/version")
def version():
    return {
        "application": "AegisOps AI",
        "version": "1.0.0",
    }


@app.post("/deployment/plan")
def create_deployment_plan(data: DeploymentRequest):
    plan = planner.create_plan(data.request)

    return {
        "status": "success",
        "request": data.request,
        "plan": plan,
    }