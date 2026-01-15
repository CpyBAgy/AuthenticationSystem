"""Сервис хеширования и проверки паролей."""
import bcrypt


class PasswordService:
    """Хеширование и проверка паролей через bcrypt."""

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Хеширует пароль."""
        if not plain_password:
            raise ValueError("Password cannot be empty")

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)

        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверяет соответствие пароля хешу."""
        if not plain_password or not hashed_password:
            raise ValueError("Passwords cannot be empty")

        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except (ValueError, AttributeError):
            return False
