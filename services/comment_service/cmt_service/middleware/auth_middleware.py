import jwt
import logging
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class MicroserviceUser:
    """A lightweight user object for microservices compatible with DRF."""
    def __init__(self, user_id, email, username):
        self.id = user_id
        self.email = email
        self.username = username

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username or self.email


class JWTAuthenticationMiddleware:
    """Custom JWT auth middleware for DRF with proper request.user assignment."""
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            with open(settings.JWT_PUBLIC_KEY_PATH, "r") as f:
                self.public_key = f.read()
            logger.info("Loaded public key successfully")
        except Exception as e:
            logger.error(f"Failed to load public key: {e}")
            raise

    def __call__(self, request):
        logger.info(f"Request hit middleware: {request.method} {request.path}")

        if request.path.startswith("/health") or request.path.startswith("/admin"):
            return self.get_response(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"detail": "Authorization header missing"}, status=401)
        if not auth_header.startswith("Bearer "):
            return JsonResponse({"detail": "Invalid authorization format"}, status=401)

        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(token, self.public_key, algorithms=["RS256"])
            logger.info(f"Decoded token: {decoded}")

            user_id = decoded.get("user_id")
            email = decoded.get("email")
            username = decoded.get("username")

            if not all([user_id, email, username]):
                return JsonResponse({"detail": "JWT missing required fields"}, status=400)

            # Assign to _user so DRF sees it correctly
            request._user = MicroserviceUser(
                user_id=user_id,
                email=email,
                username=username
            )

        except jwt.ExpiredSignatureError:
            return JsonResponse({"detail": "Token expired"}, status=401)
        except jwt.InvalidTokenError as e:
            logger.error(f"JWT decode failed: {e}")
            return JsonResponse({"detail": "Invalid token"}, status=401)
        except Exception as e:
            logger.error(f"Unexpected error decoding JWT: {e}")
            return JsonResponse({"detail": "Invalid or expired token"}, status=401)

        return self.get_response(request)
