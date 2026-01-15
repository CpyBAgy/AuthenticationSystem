"""Команда загрузки тестовых данных."""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.users.models import User
from apps.permissions.models import Role, BusinessElement, AccessRule, UserRole
from apps.authentication.services.password_service import PasswordService


class Command(BaseCommand):
    help = 'Load test data'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Loading test data...")

        self.stdout.write("Business elements...")
        elements = {
            'users': BusinessElement.objects.get_or_create(
                code='users',
                defaults={'name': 'Users', 'description': 'User management'}
            )[0],
            'products': BusinessElement.objects.get_or_create(
                code='products',
                defaults={'name': 'Products', 'description': 'Product catalog'}
            )[0],
            'orders': BusinessElement.objects.get_or_create(
                code='orders',
                defaults={'name': 'Orders', 'description': 'Order management'}
            )[0],
            'access_rules': BusinessElement.objects.get_or_create(
                code='access_rules',
                defaults={'name': 'Access Rules', 'description': 'RBAC rules'}
            )[0],
        }
        self.stdout.write(self.style.SUCCESS(f"✓ {len(elements)} elements"))

        self.stdout.write("Roles...")
        roles = {
            'admin': Role.objects.get_or_create(name='admin', defaults={'description': 'Admin', 'is_system': True})[0],
            'manager': Role.objects.get_or_create(name='manager', defaults={'description': 'Manager', 'is_system': True})[0],
            'user': Role.objects.get_or_create(name='user', defaults={'description': 'User', 'is_system': True})[0],
            'guest': Role.objects.get_or_create(name='guest', defaults={'description': 'Guest', 'is_system': True})[0],
        }
        self.stdout.write(self.style.SUCCESS(f"✓ {len(roles)} roles"))

        self.stdout.write("Access rules...")
        access_rules = [
            (roles['admin'], elements['users'], True, True, True, True, True, True, True),
            (roles['admin'], elements['products'], True, True, True, True, True, True, True),
            (roles['admin'], elements['orders'], True, True, True, True, True, True, True),
            (roles['admin'], elements['access_rules'], True, True, True, True, True, True, True),
            (roles['manager'], elements['products'], True, True, True, True, False, True, False),
            (roles['manager'], elements['orders'], True, True, True, True, False, True, False),
            (roles['user'], elements['products'], True, True, False, False, False, False, False),
            (roles['user'], elements['orders'], True, False, True, True, False, True, False),
            (roles['guest'], elements['products'], True, True, False, False, False, False, False),
        ]

        for role, element, read, read_all, create, update, update_all, delete, delete_all in access_rules:
            AccessRule.objects.get_or_create(
                role=role, element=element,
                defaults={'can_read': read, 'can_read_all': read_all, 'can_create': create,
                         'can_update': update, 'can_update_all': update_all, 'can_delete': delete, 'can_delete_all': delete_all}
            )

        self.stdout.write(self.style.SUCCESS(f"✓ {len(access_rules)} rules"))

        self.stdout.write("Users...")
        test_users = [
            ('admin@test.com', 'Admin123!', 'Admin', 'User', None, roles['admin']),
            ('manager@test.com', 'Manager123!', 'Manager', 'User', None, roles['manager']),
            ('user1@test.com', 'User123!', 'Regular', 'User', '1', roles['user']),
            ('guest@test.com', 'Guest123!', 'Guest', 'User', None, roles['guest']),
        ]

        for email, password, first_name, last_name, middle_name, role in test_users:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'last_name': last_name, 'middle_name': middle_name}
            )

            user.password = PasswordService.hash_password(password)
            user.save()

            UserRole.objects.get_or_create(user=user, role=role)

        self.stdout.write(self.style.SUCCESS("✓ Test data loaded!"))
