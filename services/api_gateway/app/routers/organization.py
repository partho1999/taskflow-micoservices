from fastapi import APIRouter, Request
import httpx
import os

router = APIRouter()

ORG_URL = os.getenv("ORG_SERVICE_URL")


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def forward_org(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        method = request.method
        body = await request.body()

        headers = dict(request.headers)
        headers.pop("host", None)

        url = f"{ORG_URL}/organization/{path}"

        response = await client.request(
            method=method,
            url=url,
            content=body,
            headers=headers
        )

        return response.json()
