"""Сервис генерации и валидации JWT токенов."""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from typing import Dict, Optional


class TokenService:
    """Создание и декодирование JWT токенов."""

    @staticmethod
    def create_access_token(user_id: int) -> str:
        """Создает access токен."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + settings.JWT_ACCESS_TOKEN_LIFETIME,
            'iat': datetime.utcnow(),
            'type': 'access'
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return token

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        """Создает refresh токен."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + settings.JWT_REFRESH_TOKEN_LIFETIME,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return token

    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        """Декодирует и валидирует токен."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token")

    @staticmethod
    def create_tokens(user_id: int) -> Dict[str, str]:
        """Создает access и refresh токены."""
        return {
            'access_token': TokenService.create_access_token(user_id),
            'refresh_token': TokenService.create_refresh_token(user_id)
        }