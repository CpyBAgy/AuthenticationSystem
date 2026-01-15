"""JWT Authentication Middleware."""
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from apps.authentication.services.auth_service import AuthService


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """Middleware для аутентификации через JWT токен."""

    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            user = AuthService.get_user_from_token(token)

            if user:
                request.user = user
            else:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        return None