"""API views для управления RBAC."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.permissions.models import Role, BusinessElement, AccessRule
from apps.permissions.serializers import RoleSerializer, BusinessElementSerializer, AccessRuleSerializer
from apps.permissions.decorators.permission_required import permission_required
from core.response import success_response, error_response


class RoleListView(APIView):
    """Список ролей."""

    @permission_required('access_rules', 'read')
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return success_response(serializer.data)

    @permission_required('access_rules', 'create')
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class RoleDetailView(APIView):
    """Детали роли."""

    @permission_required('access_rules', 'read')
    def get(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
            serializer = RoleSerializer(role)
            return success_response(serializer.data)
        except Role.DoesNotExist:
            return error_response("Role not found", status_code=status.HTTP_404_NOT_FOUND)

    @permission_required('access_rules', 'update')
    def patch(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
            serializer = RoleSerializer(role, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(serializer.data)
            return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except Role.DoesNotExist:
            return error_response("Role not found", status_code=status.HTTP_404_NOT_FOUND)

    @permission_required('access_rules', 'delete')
    def delete(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
            if role.is_system:
                return error_response("Cannot delete system role", status_code=status.HTTP_400_BAD_REQUEST)
            role.delete()
            return success_response(message="Role deleted")
        except Role.DoesNotExist:
            return error_response("Role not found", status_code=status.HTTP_404_NOT_FOUND)


class BusinessElementListView(APIView):
    """Список бизнес-элементов."""

    @permission_required('access_rules', 'read')
    def get(self, request):
        elements = BusinessElement.objects.all()
        serializer = BusinessElementSerializer(elements, many=True)
        return success_response(serializer.data)

    @permission_required('access_rules', 'create')
    def post(self, request):
        serializer = BusinessElementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class BusinessElementDetailView(APIView):
    """Детали бизнес-элемента."""

    @permission_required('access_rules', 'read')
    def get(self, request, element_id):
        try:
            element = BusinessElement.objects.get(id=element_id)
            serializer = BusinessElementSerializer(element)
            return success_response(serializer.data)
        except BusinessElement.DoesNotExist:
            return error_response("Business element not found", status_code=status.HTTP_404_NOT_FOUND)

    @permission_required('access_rules', 'update')
    def patch(self, request, element_id):
        try:
            element = BusinessElement.objects.get(id=element_id)
            serializer = BusinessElementSerializer(element, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(serializer.data)
            return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except BusinessElement.DoesNotExist:
            return error_response("Business element not found", status_code=status.HTTP_404_NOT_FOUND)

    @permission_required('access_rules', 'delete')
    def delete(self, request, element_id):
        try:
            element = BusinessElement.objects.get(id=element_id)
            element.delete()
            return success_response(message="Business element deleted")
        except BusinessElement.DoesNotExist:
            return error_response("Business element not found", status_code=status.HTTP_404_NOT_FOUND)


class AccessRuleListView(APIView):
    """Список правил доступа."""

    @permission_required('access_rules', 'read')
    def get(self, request):
        rules = AccessRule.objects.select_related('role', 'element').all()
        serializer = AccessRuleSerializer(rules, many=True)
        return success_response(serializer.data)

    @permission_required('access_rules', 'create')
    def post(self, request):
        serializer = AccessRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class AccessRuleDetailView(APIView):
    """Детали правила доступа."""

    @permission_required('access_rules', 'read')
    def get(self, request, rule_id):
        try:
            rule = AccessRule.objects.select_related('role', 'element').get(id=rule_id)
            serializer = AccessRuleSerializer(rule)
            return success_response(serializer.data)
        except AccessRule.DoesNotExist:
            return error_response("Access rule not found", status_code=status.HTTP_404_NOT_FOUND)

    @permission_required('access_rules', 'update')
    def patch(self, request, rule_id):
        try:
            rule = AccessRule.objects.get(id=rule_id)
            serializer = AccessRuleSerializer(rule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(serializer.data)
            return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except AccessRule.DoesNotExist:
            return error_response("Access rule not found", status_code=status.HTTP_404_NOT_FOUND)

    @permission_required('access_rules', 'delete')
    def delete(self, request, rule_id):
        try:
            rule = AccessRule.objects.get(id=rule_id)
            rule.delete()
            return success_response(message="Access rule deleted")
        except AccessRule.DoesNotExist:
            return error_response("Access rule not found", status_code=status.HTTP_404_NOT_FOUND)