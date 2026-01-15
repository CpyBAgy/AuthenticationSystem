"""URL configuration for config project."""
from django.urls import path, include
from core.views import WelcomeView, APITestView

urlpatterns = [
    path("", WelcomeView.as_view(), name="welcome"),
    path("test/", APITestView.as_view(), name="api-test"),
    path("api/auth/", include("apps.authentication.urls")),
    path("api/users/", include("apps.users.urls")),
    path("api/admin/", include("apps.permissions.urls")),
    path("api/", include("apps.mock_resources.urls")),
]