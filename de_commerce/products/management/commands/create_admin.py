"""
Management command to create a superuser/staff admin account for product uploads.

This command creates an admin account with superuser and staff privileges,
allowing them to upload and manage products via the dedicated admin API endpoint.

Usage:
    python manage.py create_admin --username admin --email admin@example.com --password securepass123
    python manage.py create_admin --username admin --email admin@example.com  # (prompts for password)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import getpass


class Command(BaseCommand):
    help = 'Create a superuser/staff admin account for product imports'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='Admin username'
        )
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Admin email'
        )
        parser.add_argument(
            '--password',
            type=str,
            default=None,
            help='Admin password (will prompt if not provided)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Prompt for password if not provided
        if not password:
            password = getpass.getpass('Enter admin password: ')
            password_confirm = getpass.getpass('Confirm admin password: ')
            if password != password_confirm:
                self.stdout.write(self.style.ERROR('Passwords do not match.'))
                return

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            return

        # Create superuser (is_staff=True and is_superuser=True)
        user = User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'✓ Admin account "{username}" created successfully.'))
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Admin can now login and access /api/admin/import-products/ endpoint.')
