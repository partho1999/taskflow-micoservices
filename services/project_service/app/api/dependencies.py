from fastapi import Depends, Header, HTTPException, status
from typing import Callable
from app.core.security import verify_jwt
from app.services.org_client import get_member


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


# -----------------------------
# Require specific organization roles
# -----------------------------
def require_org_role(required_roles: list[str]) -> Callable:
    """
    Dependency factory to enforce organization roles.
    Usage: Depends(require_org_role(["owner", "admin"]))
    """
    def dependency(org_id: str, user: dict = Depends(get_current_user)) -> dict:
        member_info = get_member(org_id, user["user_id"], user["token"])
        if member_info["role"].lower() not in [role.lower() for role in required_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role",
            )
        return {
            "user_id": user["user_id"],
            "role": member_info["role"],
            "org_id": org_id,
        }

    return dependency
