import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_countries import countries
from faker import Faker

from core.models import Role
from ecommerce.models import Order, OrderItem, Product, ProductCategory, ShippingAddress

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Load sample ecommerce data."

    def _load_shipping_addresses(self):
        if ShippingAddress.objects.exists():
            return self.stdout.write(
                self.style.SUCCESS(
                    "Some shipping addresses already exist. Aborting loading sample objects."
                )
            )

        for user in User.objects.filter(role=Role.CUSTOMER):
            ShippingAddress.objects.create(
                user=user,
                full_name=fake.name(),
                street=fake.street_address(),
                zip_code=fake.postcode(),
                city=fake.city(),
                country=random.choice(countries),
            )
        self.stdout.write(self.style.SUCCESS("Sample shipping adddresses loaded."))

    def _load_products(self, categories, n=1):
        if Product.objects.exists():
            return self.stdout.write(
                self.style.SUCCESS("Some products already exist. Aborting loading sample objects.")
            )

        for category_name in categories:
            category, created = ProductCategory.objects.get_or_create(name=category_name)
            product_name = category_name[:-1]
            products = [
                Product(
                    name=f"{product_name} {i}",
                    description=f"Description of {product_name} {i}",
                    price=random.randint(100, 5000) + 0.99,
                    category=category,
                )
                for i in range(1, n + 1)
            ]
            Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS("Sample products loaded."))

    def _load_orders(self, n=1):
        if Order.objects.exists():
            return self.stdout.write(
                self.style.SUCCESS("Some orders already exist. Aborting loading sample objects.")
            )

        for user in User.objects.filter(role=Role.CUSTOMER):
            for _ in range(1, n + 1):
                order = Order.objects.create(
                    user=user, shipping_address=user.shipping_addresses.last()
                )

                products = Product.objects.all().order_by("?")
                OrderItem.objects.create(
                    order=order, product=products.first(), quantity=random.randint(1, 3)
                )
                OrderItem.objects.create(
                    order=order, product=products.last(), quantity=random.randint(1, 3)
                )

        self.stdout.write(self.style.SUCCESS("Sample orders loaded."))

    def handle(self, *args, **kwargs):
        self._load_shipping_addresses()
        self._load_products(
            categories=["Computers", "Smartphones", "Peripherals", "Consoles"], n=5
        )
        self._load_orders(n=3)
