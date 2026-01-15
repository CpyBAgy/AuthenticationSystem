"""
URL configuration for users app.
"""
from django.urls import path
from apps.users.views import UserProfileView

app_name = 'users'

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='profile'),
]