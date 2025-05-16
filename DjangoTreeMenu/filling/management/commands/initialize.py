"""Command for fill database with base information."""

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Fill database with Default admin."""

    help = __doc__

    def handle(self, *args, **options):
        """Proccess command."""
        # Create default Admin
        deafult_admin = User.objects.create(
            email=settings.ADMIN_EMAIL,
            username=settings.ADMIN_USERNAME,
            is_staff=True,
            is_superuser=True,
        )
        deafult_admin.set_password(settings.ADMIN_PASSWORD)
        deafult_admin.save()
