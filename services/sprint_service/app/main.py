from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api.sprint import router as sprint_router
# future routers
# from app.api.milestone import router as milestone_router
# from app.api.progress import router as progress_router

# -----------------------------
# Initialize FastAPI App
# -----------------------------
app = FastAPI(
    title="Sprint Service",
    description="Microservice for managing sprints, milestones, and progress tracking",
    version="1.0.0",
)

# -----------------------------
# CORS Middleware
# -----------------------------
# Allow all origins for now; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(
    sprint_router,
    prefix="/api/sprints",
    tags=["Sprints"],
)

# Uncomment when ready
# app.include_router(milestone_router, prefix="/api/milestones", tags=["Milestones"])
# app.include_router(progress_router, prefix="/api/progress", tags=["Progress"])

# -----------------------------
# Health Check
# -----------------------------
@app.get("/", tags=["Health"])
def root():
    """
    Root health check endpoint.
    Returns service status.
    """
    return {"service": "sprint_service", "status": "running"}
