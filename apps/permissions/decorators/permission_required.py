"""Декоратор проверки прав доступа."""
from functools import wraps
from rest_framework import status
from apps.permissions.services.permission_service import PermissionService
from core.response import error_response


def permission_required(resource_code: str, action: str, check_ownership: bool = False):
    """Проверяет права пользователя на действие с ресурсом."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(view_instance, request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return error_response(
                    message="Authentication required",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

            resource_owner_id = None
            if check_ownership:
                resource_owner_id = (
                    getattr(request, 'resource_owner_id', None) or
                    request.data.get('owner_id') or
                    kwargs.get('owner_id')
                )

            has_permission = PermissionService.check_permission(
                user=request.user,
                resource_code=resource_code,
                action=action,
                resource_owner_id=resource_owner_id
            )

            if not has_permission:
                return error_response(
                    message=f"You do not have permission to {action} {resource_code}",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            return view_func(view_instance, request, *args, **kwargs)

        return wrapper
    return decorator