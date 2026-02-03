from fastapi import APIRouter, Request, Response
import httpx
import os

router = APIRouter()
AUTH_URL = os.getenv("AUTH_SERVICE_URL")


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def forward_auth(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        method = request.method
        body = await request.body()

        # Copy headers except host
        headers = dict(request.headers)
        headers.pop("host", None)

        url = f"{AUTH_URL}/auth/{path}"

        response = await client.request(
            method=method,
            url=url,
            content=body,
            headers=headers
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )
