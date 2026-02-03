import httpx
from fastapi import Request, HTTPException

async def forward_request(request: Request, url: str):
    """
    Forward client request to a microservice and return the response.
    """

    # Extract method (GET, POST, PUT, DELETE)
    method = request.method

    # Extract query params
    params = request.query_params

    # Extract body (JSON, form, anything)
    try:
        body = await request.json()
    except:
        body = None

    # Extract headers
    headers = dict(request.headers)
    headers.pop("host", None)  # remove host header to avoid conflicts

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                params=params,
                json=body,
                headers=headers,
                timeout=10.0
            )

        return response
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Service unavailable: {str(e)}"
        )
