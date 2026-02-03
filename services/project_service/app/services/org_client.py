import requests
from fastapi import HTTPException, status
from app.core.config import settings

# Base URL for organization service
ORG_SERVICE_URL = f"{settings.ORG_SERVICE_URL}/api/org"  # e.g., http://organization_service:8001/api/org

def get_member(org_id: str, user_id: str, token: str) -> dict:
    """
    Call organization service to get a single member by org_id and user_id.
    Raises HTTPException if not found or service fails.
    """
    url = f"{ORG_SERVICE_URL}/{org_id}/members/user/{user_id}/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Host": "localhost"  # Important to match Traefik/Django routing
    }

    print(">>>> URL:", url)
    print(">>>> HEADERS:", headers)

    try:
        r = requests.get(url, headers=headers, timeout=5)
    except requests.ConnectionError as e:
        print("Connection error:", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot connect to organization service: {e}"
        )
    except requests.Timeout as e:
        print("Timeout error:", e)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Organization service request timed out: {e}"
        )
    except requests.RequestException as e:
        print("Other request exception:", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Organization service request failed: {e}"
        )

    print(">>>> RESPONSE STATUS:", r.status_code)
    print(">>>> RESPONSE TEXT:", r.text)

    # Handle not found
    if r.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization"
        )
    
    # Handle other non-200 errors
    if r.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Organization service error: {r.status_code}"
        )

    # Parse JSON response
    try:
        data = r.json()  # expected: {"user_id": ..., "role": ...}
    except ValueError as e:
        print("JSON decode error:", e)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid JSON response from organization service"
        )

    # Ensure role is lowercase to match internal checks
    if "role" in data:
        data["role"] = data["role"].lower()

    return data
