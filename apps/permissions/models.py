"""RBAC модели."""
from django.db import models
from django.conf import settings


class Role(models.Model):
    """Роль в RBAC системе."""
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'
        ordering = ['name']

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    """Бизнес-элементы (ресурсы)."""
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'business_elements'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class AccessRule(models.Model):
    """Правила доступа для ролей."""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='access_rules')
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE, related_name='access_rules')

    can_read = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'access_rules'
        unique_together = [['role', 'element']]
        ordering = ['role__name', 'element__name']

    def __str__(self):
        return f"{self.role.name} -> {self.element.code}"


class UserRole(models.Model):
    """Связь пользователей и ролей."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        unique_together = [['user', 'role']]
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.user.email} has role {self.role.name}"
