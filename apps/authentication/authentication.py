"""JWT аутентификация для DRF."""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.authentication.services.auth_service import AuthService


class JWTAuthentication(BaseAuthentication):
    """JWT аутентификация через Bearer токен."""
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        try:
            parts = auth_header.split()

            if len(parts) == 0:
                return None

            if parts[0].lower() != self.keyword.lower():
                return None

            if len(parts) == 1:
                raise AuthenticationFailed('Invalid token header. No credentials provided.')

            if len(parts) > 2:
                raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

            token = parts[1]

            user = AuthService.get_user_from_token(token)

            if not user:
                raise AuthenticationFailed('Invalid or expired token.')

            return (user, token)

        except AuthenticationFailed:
            raise
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

    def authenticate_header(self, request):
        return self.keyword
