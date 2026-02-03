# tests/test_org_member_request.py
import os
import requests

# Get environment variable inside container
ORG_SERVICE_URL = os.getenv("ORG_SERVICE_URL", "http://organization_service:8001")

# Example IDs
org_id = "4567a554-2c2d-4025-9c6f-917688d75787"
user_id = "7eb7ced3-7519-4b68-9c8c-2051117f64e4"

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2MzE0MjAwLCJpYXQiOjE3NjYzMTA2MDAsImp0aSI6IjY4YmYyNzUwZTNkZTRkN2ZhNGM5OWE3NTg4MjM3YjQwIiwidXNlcl9pZCI6IjdlYjdjZWQzLTc1MTktNGI2OC05YzhjLTIwNTExMTdmNjRlNCJ9.EVwRpiwJTJYws59hh36Pd_CfnRCiR-YxzJOS1Wv5nxcQ-V89W49heRpNPY3oJlaOWT6BbhbAsMfjJEv7edeTHYUBvbDi8m51bvVwffPhZKhmKV2aR05MdrOL3krbpA4EMxNnN13Xf0TJaF8LUhnqiJ4Q5G42zfvUdHBV_Qm8dqRHLkxcu8C-fo9KTQvAaLYRRFvsRAxrPJp9CdAztwhpi0YNF6Mcsmfzfy09aFkzCaz4pokGbMKm5duV5zfN1JY2koAr1HB7VzKull3gXKhi7JL30Z4hNx5TtqGQB4QjW7XKceD3b_hcGWShpMni7vXtnAbocDb4FFlye0mvJksgtA"  # Use a valid JWT

url = f"{ORG_SERVICE_URL}/api/org/{org_id}/members/user/{user_id}"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",  # Ensure JSON response
}

print(">>>> URL:", url)
print(">>>> HEADERS:", headers)

try:
    r = requests.get(url, headers=headers, timeout=5)
    print(">>>> RESPONSE STATUS:", r.status_code)
    print(">>>> RESPONSE TEXT:", r.text)
except requests.RequestException as e:
    print(">>>> REQUEST ERROR:", e)
