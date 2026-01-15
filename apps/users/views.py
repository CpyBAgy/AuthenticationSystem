"""API views для управления пользователями."""
from rest_framework.views import APIView
from rest_framework import status
from apps.users.serializers import UserProfileSerializer, UpdateUserSerializer
from core.response import success_response, error_response


class UserProfileView(APIView):
    """Управление профилем пользователя."""

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return error_response(
                message="Authentication required",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        serializer = UserProfileSerializer(request.user)

        return success_response(
            data=serializer.data,
            message="User profile retrieved successfully"
        )

    def patch(self, request):
        if not request.user or not request.user.is_authenticated:
            return error_response(
                message="Authentication required",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        serializer = UpdateUserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        profile_serializer = UserProfileSerializer(request.user)

        return success_response(
            data=profile_serializer.data,
            message="User profile updated successfully"
        )

    def delete(self, request):
        if not request.user or not request.user.is_authenticated:
            return error_response(
                message="Authentication required",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        request.user.is_active = False
        request.user.save()

        return success_response(
            message="User account has been deactivated successfully",
            status_code=status.HTTP_200_OK
        )
