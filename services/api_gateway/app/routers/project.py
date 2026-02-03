from fastapi import APIRouter, Request
from app.core.proxy import forward_request
from app.config import PROJECT_SERVICE_URL

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_projects(request: Request, path: str):
    target_url = f"{PROJECT_SERVICE_URL}/{path}"
    response = await forward_request(request, target_url)
    return response.json()
