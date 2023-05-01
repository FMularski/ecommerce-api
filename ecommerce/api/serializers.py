from datetime import timedelta

from rest_framework import serializers

from ecommerce import tasks
from ecommerce.models import Order, OrderItem, Product, ProductCategory, ShippingAddress


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ReadonlyProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = Product
        exclude = ("image_min",)


class ReadonlyProductSerializer(serializers.ModelSerializer):
    category = ReadonlyProductCategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = "id", "order"


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        exclude = (
            "id",
            "user",
        )


class OrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "total_price", "payment_deadline"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        exclude = "id", "created_at", "payment_deadline", "user"

    def _send_order_confirmation(self, order):
        tasks.queue_email.delay(
            temp_subject="ecommerce/email/order_confirm_subject.txt",
            temp_html="ecommerce/email/order_confirm.html",
            temp_str="ecommerce/email/order_confirm.txt",
            context={
                "order": str(order),
                "items": [
                    {
                        "name": item.product.name,
                        "price": item.product.price,
                        "quantity": item.quantity,
                    }
                    for item in order.items.all()
                ],
                "total": order.total_price,
                "payment_deadline": order.payment_deadline,
            },
            recipients=[order.user.email],
        )

    def _queue_payment_reminder(self, order):
        tasks.queue_email.apply_async(
            kwargs={
                "temp_subject": "ecommerce/email/payment_reminder_subject.txt",
                "temp_html": "ecommerce/email/payment_reminder.html",
                "temp_str": "ecommerce/email/payment_reminder.txt",
                "context": {
                    "order": str(order),
                    "total": order.total_price,
                    "payment_deadline": order.payment_deadline,
                },
                "recipients": [order.user.email],
            },
            eta=order.payment_deadline + timedelta(days=1),
        )

    def create(self, validated_data):
        user = self.context["request"].user
        items = validated_data.pop("items")
        shipping_address = validated_data.pop("shipping_address")

        address, address_created = ShippingAddress.objects.get_or_create(
            **(shipping_address | {"user": user})
        )
        order = Order.objects.create(
            **(validated_data | {"shipping_address": address, "user": user})
        )

        items = [OrderItem(**(item_data | {"order": order})) for item_data in items]
        OrderItem.objects.bulk_create(items)

        self._send_order_confirmation(order)
        self._queue_payment_reminder(order)

        return order

    def to_representation(self, instance):
        response_serializer = OrderResponseSerializer(instance)
        return response_serializer.data
