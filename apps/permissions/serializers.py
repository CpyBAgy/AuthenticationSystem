"""Serializers для RBAC моделей."""
from rest_framework import serializers
from apps.permissions.models import Role, BusinessElement, AccessRule


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'is_system', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ['id', 'code', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccessRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    element_code = serializers.CharField(source='element.code', read_only=True)

    class Meta:
        model = AccessRule
        fields = [
            'id', 'role', 'role_name', 'element', 'element_code',
            'can_read', 'can_read_all', 'can_create',
            'can_update', 'can_update_all',
            'can_delete', 'can_delete_all',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']