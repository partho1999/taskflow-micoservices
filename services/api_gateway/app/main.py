from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.organization import router as org_router
# from app.routers.project import router as project_router


def create_app():
    app = FastAPI(
        title="TaskFlow API Gateway",
        version="1.0.0",
        description="Central API gateway for all microservices"
    )

    # CORS (allow frontend access)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],      # in production specify frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include all routes
    app.include_router(auth_router, prefix="/auth", tags=["Auth Service"])
    app.include_router(org_router, prefix="/organization", tags=["Organization Service"])
    # app.include_router(project_router, prefix="/projects", tags=["Project Service"])

    return app


app = create_app()
