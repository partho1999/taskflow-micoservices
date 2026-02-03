from rest_framework_simplejwt.authentication import JWTAuthentication
from types import SimpleNamespace

class MicroserviceUser(SimpleNamespace):
    @property
    def is_authenticated(self):
        return True


class MicroserviceJWTAuthentication(JWTAuthentication):
    """
    Custom authentication for microservice where User does not exist locally.
    """

    def get_user(self, validated_token):
        # Extract user ID from token (default claim: "user_id")
        user_id = validated_token.get("user_id")

        # Return a fake DRF user object that behaves like a logged-in user
        return MicroserviceUser(id=user_id)
