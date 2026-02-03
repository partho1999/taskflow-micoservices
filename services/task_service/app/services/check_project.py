import requests
from fastapi import HTTPException, status
from app.core.config import settings

# Base URL for project service
PROJECT_SERVICE_URL = f"{settings.PROJECT_SERVICE_URL}/api/projects"  # e.g., http://project_service:8002/api/projects

def get_project(project_id: str, token: str) -> dict:
    """
    Fetch project from Project Service and return key identifiers.
    Returns:
        {
            "id": str,
            "org_id": str,
            "owner_id": str
        }
    Raises HTTPException on failure.
    """
    url = f"{PROJECT_SERVICE_URL}/{project_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()  # raise for HTTP errors
    except requests.HTTPError as e:
        if r.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Project service error: {r.status_code}"
            )
    except requests.ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot connect to Project Service: {e}"
        )
    except requests.Timeout as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Project Service request timed out: {e}"
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Project Service request failed: {e}"
        )

    # Parse JSON response
    try:
        data = r.json()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid JSON response from Project Service"
        )

    # Return only the IDs needed for Task Service
    return {
        "id": data["id"],
        "org_id": data["org_id"],
        "owner_id": data["owner_id"]
    }
