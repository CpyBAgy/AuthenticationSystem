"""Сервис проверки прав доступа RBAC."""
from typing import Optional
from apps.users.models import User
from apps.permissions.models import AccessRule, BusinessElement


class PermissionService:
    """Проверка прав пользователя на основе RBAC."""

    @staticmethod
    def check_permission(
        user: User,
        resource_code: str,
        action: str,
        resource_owner_id: Optional[int] = None
    ) -> bool:
        """Проверяет право пользователя на действие с ресурсом."""
        if not user or not user.is_authenticated or not user.is_active:
            return False

        try:
            element = BusinessElement.objects.get(code=resource_code)
        except BusinessElement.DoesNotExist:
            return False

        user_roles = user.user_roles.select_related('role').all()

        if not user_roles.exists():
            return False

        for user_role in user_roles:
            role = user_role.role

            try:
                rule = AccessRule.objects.get(role=role, element=element)
            except AccessRule.DoesNotExist:
                continue

            if action == 'read':
                if rule.can_read_all:
                    return True
                if rule.can_read:
                    if resource_owner_id is None or resource_owner_id == user.id:
                        return True

            elif action == 'create':
                if rule.can_create:
                    return True

            elif action == 'update':
                if rule.can_update_all:
                    return True
                if rule.can_update:
                    if resource_owner_id is None or resource_owner_id == user.id:
                        return True

            elif action == 'delete':
                if rule.can_delete_all:
                    return True
                if rule.can_delete:
                    if resource_owner_id is None or resource_owner_id == user.id:
                        return True

        return False

    @staticmethod
    def can_read(user: User, resource_code: str, resource_owner_id: Optional[int] = None) -> bool:
        return PermissionService.check_permission(user, resource_code, 'read', resource_owner_id)

    @staticmethod
    def can_create(user: User, resource_code: str) -> bool:
        return PermissionService.check_permission(user, resource_code, 'create')

    @staticmethod
    def can_update(user: User, resource_code: str, resource_owner_id: Optional[int] = None) -> bool:
        return PermissionService.check_permission(user, resource_code, 'update', resource_owner_id)

    @staticmethod
    def can_delete(user: User, resource_code: str, resource_owner_id: Optional[int] = None) -> bool:
        return PermissionService.check_permission(user, resource_code, 'delete', resource_owner_id)
