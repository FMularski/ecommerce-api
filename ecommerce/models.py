from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

User = get_user_model()


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipping_addresses")
    full_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = CountryField()

    def __str__(self):
        return f"""
        {self.street}
        {self.city} {self.zip_code}
        {self.country.name}
        """


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # up to 9999.99
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name="products"
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.PROTECT, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    payment_deadline = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.payment_at:
            self.payment_at = self.created_at + timedelta(days=5)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return _("Order") + str(self.pk).zfill(4)

    @property
    def total_price(self):
        return sum([item.product.price for item in self.items])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"[{self.order}] {self.product} x{self.quantity}"
