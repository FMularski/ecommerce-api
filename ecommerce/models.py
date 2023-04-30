import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from PIL import Image

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
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator]
    )  # up to 9999.99
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name="products"
    )

    IMAGE_FULL_DIR = "full/"
    IMAGE_MINI_DIR = "mini/"

    image = models.ImageField(upload_to=IMAGE_FULL_DIR)
    image_min = models.ImageField(upload_to=IMAGE_MINI_DIR, blank=True)

    def create_image_min(self):
        """
        Creating miniature image based on the full-sized pic
        """
        if not os.path.exists(settings.MEDIA_URL[1:] + self.IMAGE_MINI_DIR):
            os.makedirs(settings.MEDIA_URL[1:] + self.IMAGE_MINI_DIR)

        open_path = settings.MEDIA_URL[1:] + self.IMAGE_FULL_DIR + self.image.name
        if self.IMAGE_FULL_DIR in self.image.name:
            open_path = settings.MEDIA_URL[1:] + self.image.name

        with Image.open(open_path) as full_image:
            min_image = full_image.resize((200, 200), Image.ANTIALIAS)

            if self.IMAGE_FULL_DIR in self.image.name:
                min_image.save("media/" + self.IMAGE_MINI_DIR + self.image.name.split("/")[1])
                self.image_min = self.IMAGE_MINI_DIR + self.image.name.split("/")[1]
            else:
                min_image.save("media/" + self.IMAGE_MINI_DIR + self.image.name)
                self.image_min = self.IMAGE_MINI_DIR + self.image.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # create a new image file if has not been created yet or a new file has been uploaded
        create_min_image = (
            not self.image.name == self.image_min.name.split("/")[1] if self.image_min else True
        )
        if create_min_image:
            self.create_image_min()

        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.PROTECT, related_name="orders"
    )
    created_at = models.DateTimeField(blank=True)
    payment_deadline = models.DateTimeField(blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.created_at:
            self.created_at = timezone.now()
            self.payment_deadline = self.created_at + timedelta(days=5)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return _("Order") + f" #{str(self.pk).zfill(4)}"

    @property
    def total_price(self):
        return sum([item.product.price for item in self.items.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"[{self.order}] {self.product} x{self.quantity}"
