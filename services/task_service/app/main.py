# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api.tasks import router as task_router
# Future routers:
from app.api.subtasks import router as subtask_router
from app.api.kanban import router as kanban_router
from app.api.leaderboard import router as leaderboard_router

# -----------------------------
# Initialize FastAPI App
# -----------------------------
app = FastAPI(
    title="Task Service",
    description="Microservice for managing tasks, subtasks, Kanban boards, and leaderboards",
    version="1.0.0",
)

# -----------------------------
# CORS Middleware
# -----------------------------
# Allow all origins for now; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
# Task CRUD endpoints
app.include_router(task_router, prefix="/api/tasks", tags=["Tasks"])

# Uncomment when ready
app.include_router(subtask_router, prefix="/api/subtasks", tags=["Subtasks"])
app.include_router(kanban_router, prefix="/api/kanban", tags=["Kanban"])
app.include_router(leaderboard_router, prefix="/api/leaderboard", tags=["Leaderboard"])

# -----------------------------
# Health Check
# -----------------------------
@app.get("/", tags=["Health"])
def root():
    """
    Root health check endpoint.
    Returns service status.
    """
    return {"service": "task_service", "status": "running"}
