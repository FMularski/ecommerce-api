from django.core.management.base import BaseCommand

from core.models import Role, User


class Command(BaseCommand):
    help = "Load sample users."

    def handle(self, *args, **kwargs):
        if User.objects.exists():
            return self.stdout.write(
                self.style.WARNING("Some users already exist. Aborting loading sample users.")
            )

        User.objects.create_superuser(email="admin@mail.com", password="admin", role=Role.SELLER)
        User.objects.create_user(email="seller@mail.com", password="seller", role=Role.SELLER)
        User.objects.create_user(
            email="customer@mail.com", password="customer", role=Role.CUSTOMER
        )

        self.stdout.write(self.style.SUCCESS("Sample users loaded."))
