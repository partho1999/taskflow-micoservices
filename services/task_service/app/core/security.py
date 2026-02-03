from pathlib import Path
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from app.core.config import settings

# Load public key
PUBLIC_KEY = Path(settings.JWT_PUBLIC_KEY_PATH).read_text()

def verify_jwt(token: str) -> dict:
    """
    Verify JWT and return payload.
    Skips issuer and audience verification (for testing).
    """
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            options={"verify_aud": False, "verify_iss": False},  # skip aud/iss
        )

        user_id = payload.get("user_id")  # extract user_id claim
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user_id missing in token",
            )

        return {"user_id": user_id, "raw_payload": payload}

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
