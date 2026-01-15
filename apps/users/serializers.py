"""Serializers для управления пользователями."""
from rest_framework import serializers
from apps.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'full_name', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'is_active', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name']

    def validate(self, data):
        if 'first_name' in data and not data['first_name'].strip():
            raise serializers.ValidationError({"first_name": "First name cannot be empty"})
        if 'last_name' in data and not data['last_name'].strip():
            raise serializers.ValidationError({"last_name": "Last name cannot be empty"})
        return data