import requests
from fastapi import HTTPException, status
from app.core.config import settings

# Base URL for task service
TASK_SERVICE_URL = f"{settings.TASK_SERVICE_URL}/api/tasks/"


def get_sprint_progress(sprint_id: str, token: str) -> dict:
    """
    Fetch tasks from Task Service and calculate sprint progress.

    Returns:
        {
            "total_tasks": int,
            "done_tasks": int,
            "progress": int
        }
    """

    url = TASK_SERVICE_URL
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "sprint_id": sprint_id
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        r.raise_for_status()
    except requests.HTTPError:
        if r.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No tasks found for sprint {sprint_id}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Task service error: {r.status_code}"
            )
    except requests.ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot connect to Task Service: {e}"
        )
    except requests.Timeout as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Task Service request timed out: {e}"
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Task Service request failed: {e}"
        )

    # Parse JSON response
    try:
        tasks = r.json()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid JSON response from Task Service"
        )

    # Calculate progress
    if not tasks:
        return {
            "total_tasks": 0,
            "done_tasks": 0,
            "progress": 0
        }

    total = len(tasks)
    done = len([t for t in tasks if t.get("status") == "done"])

    progress = int((done / total) * 100)

    return {
        "total_tasks": total,
        "done_tasks": done,
        "progress": progress
    }
