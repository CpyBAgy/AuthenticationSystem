"""Сервис управления ролями."""
from typing import List
from django.db import transaction
from apps.users.models import User
from apps.permissions.models import Role, UserRole
from core.exceptions import ValidationError


class RoleService:
    """Управление ролями пользователей."""

    @staticmethod
    @transaction.atomic
    def assign_role(user: User, role: Role, assigned_by: User = None) -> UserRole:
        """Назначает роль пользователю."""
        if UserRole.objects.filter(user=user, role=role).exists():
            raise ValidationError(f"Role '{role.name}' is already assigned to user")

        user_role = UserRole.objects.create(
            user=user,
            role=role,
            assigned_by=assigned_by
        )

        return user_role

    @staticmethod
    @transaction.atomic
    def revoke_role(user: User, role: Role) -> bool:
        """Отзывает роль у пользователя."""
        try:
            user_role = UserRole.objects.get(user=user, role=role)

            if user.user_roles.count() == 1:
                raise ValidationError("Cannot revoke the last role from a user")

            user_role.delete()
            return True

        except UserRole.DoesNotExist:
            return False

    @staticmethod
    def get_user_roles(user: User) -> List[Role]:
        """Возвращает роли пользователя."""
        return [ur.role for ur in user.user_roles.select_related('role').all()]

    @staticmethod
    def user_has_role(user: User, role_name: str) -> bool:
        """Проверяет наличие роли у пользователя."""
        return user.user_roles.filter(role__name=role_name).exists()