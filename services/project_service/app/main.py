from fastapi import FastAPI
from app.api.projects import router as project_router
from app.api.project_members import router as project_member_router

app = FastAPI(title="Project Service")

app.include_router(project_router, prefix="/api/projects", tags=["Projects"])
app.include_router(project_member_router, prefix="/api/projects/members", tags=["projects-members"])
