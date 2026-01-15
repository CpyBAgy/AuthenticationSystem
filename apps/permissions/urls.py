"""URL configuration for permissions app."""
from django.urls import path
from apps.permissions.views import (
    RoleListView,
    RoleDetailView,
    BusinessElementListView,
    BusinessElementDetailView,
    AccessRuleListView,
    AccessRuleDetailView
)

app_name = 'permissions'

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('roles/<int:role_id>/', RoleDetailView.as_view(), name='role-detail'),
    path('business-elements/', BusinessElementListView.as_view(), name='business-element-list'),
    path('business-elements/<int:element_id>/', BusinessElementDetailView.as_view(), name='business-element-detail'),
    path('access-rules/', AccessRuleListView.as_view(), name='access-rule-list'),
    path('access-rules/<int:rule_id>/', AccessRuleDetailView.as_view(), name='access-rule-detail'),
]