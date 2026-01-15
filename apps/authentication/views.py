"""API views для аутентификации."""
from rest_framework.views import APIView
from rest_framework import status
from apps.authentication.serializers import (
    RegisterSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    TokenResponseSerializer,
    UserSerializer
)
from apps.authentication.services.auth_service import AuthService
from core.response import success_response, error_response
from core.exceptions import AuthenticationFailed, ValidationError, UserInactive


class RegisterView(APIView):
    """Регистрация пользователя."""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = AuthService.register(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                middle_name=serializer.validated_data.get('middle_name')
            )

            user_serializer = UserSerializer(user)

            return success_response(
                data={'user': user_serializer.data},
                message="User registered successfully",
                status_code=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return error_response(
                message="Registration failed",
                errors={'detail': str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    """Вход пользователя."""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = AuthService.login(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            user_serializer = UserSerializer(result['user'])
            response_data = {
                'user': user_serializer.data,
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token']
            }

            return success_response(
                data=response_data,
                message="Login successful",
                status_code=status.HTTP_200_OK
            )

        except (AuthenticationFailed, UserInactive) as e:
            return error_response(
                message=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return error_response(
                message="Login failed",
                errors={'detail': str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshTokenView(APIView):
    """Обновление access токена."""

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = AuthService.refresh_access_token(
                refresh_token=serializer.validated_data['refresh_token']
            )

            return success_response(
                data=result,
                message="Token refreshed successfully",
                status_code=status.HTTP_200_OK
            )

        except AuthenticationFailed as e:
            return error_response(
                message=str(e),
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return error_response(
                message="Token refresh failed",
                errors={'detail': str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    """Выход пользователя (JWT stateless - удаление токенов на клиенте)."""

    def post(self, request):
        return success_response(
            message="Logout successful. Please delete tokens on client side.",
            status_code=status.HTTP_200_OK
        )
