from fastapi import Depends, Header, HTTPException, status
from typing import Callable
from app.core.security import verify_jwt
from app.services.check_project import get_project


# -----------------------------
# Get current user from Authorization header
# -----------------------------
def get_current_user(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )

    token = authorization.split(" ")[1]
    payload = verify_jwt(token)

    return {
        "user_id": payload["user_id"],  # extracted from JWT
        "token": token,
    }


def check_project() -> Callable:
    """
    Dependency to fetch project info by project_id from URL.
    Returns project info if successful.
    Raises HTTPException if project does not exist or service fails.
    """
    def dependency(project_id: str, user: dict = Depends(get_current_user)) -> dict:
        # project_id comes automatically from the URL
        project_info = get_project(project_id, token=user["token"])
        return project_info

    return dependency