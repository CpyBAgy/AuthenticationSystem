"""Сервис аутентификации пользователей."""
from typing import Dict, Optional
from django.db import transaction
from apps.users.models import User
from apps.authentication.services.password_service import PasswordService
from apps.authentication.services.token_service import TokenService
from core.exceptions import (
    AuthenticationFailed,
    ValidationError,
    UserInactive
)


class AuthService:
    """Обработка операций аутентификации."""

    @staticmethod
    @transaction.atomic
    def register(
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        middle_name: Optional[str] = None,
        created_by: Optional[User] = None
    ) -> User:
        """Регистрация нового пользователя."""
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"User with email {email} already exists")

        if not password or len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        hashed_password = PasswordService.hash_password(password)

        user = User.objects.create_user(
            email=email,
            password=None,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            created_by=created_by
        )

        user.password = hashed_password
        user.save()

        return user

    @staticmethod
    def login(email: str, password: str) -> Dict[str, any]:
        """Аутентификация и генерация токенов."""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password")

        if not user.is_active:
            raise UserInactive("User account is inactive")

        if not PasswordService.verify_password(password, user.password):
            raise AuthenticationFailed("Invalid email or password")

        tokens = TokenService.create_tokens(user.id)

        return {
            'user': user,
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }

    @staticmethod
    def refresh_access_token(refresh_token: str) -> Dict[str, str]:
        """Обновление access токена через refresh токен."""
        import jwt

        try:
            payload = TokenService.decode_token(refresh_token)

            if payload.get('type') != 'refresh':
                raise AuthenticationFailed("Invalid token type")

            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed("Invalid token payload")

            try:
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                raise AuthenticationFailed("User not found or inactive")

            access_token = TokenService.create_access_token(user.id)

            return {
                'access_token': access_token
            }

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            raise AuthenticationFailed(f"Invalid refresh token: {str(e)}")

    @staticmethod
    def get_user_from_token(token: str) -> Optional[User]:
        """Извлечение пользователя из JWT токена."""
        import jwt

        try:
            payload = TokenService.decode_token(token)
            user_id = payload.get('user_id')

            if not user_id:
                return None

            user = User.objects.get(id=user_id, is_active=True)
            return user

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None