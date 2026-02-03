from fastapi import Depends, Header, HTTPException, status
from typing import Callable
from app.core.security import verify_jwt



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
