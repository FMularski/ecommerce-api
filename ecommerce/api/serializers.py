from rest_framework import serializers

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

        # schedule celery tasks:
        # send notification email (instant)
        # schedule a reminder email (1 day before payment_deadline)

        return order

    def to_representation(self, instance):
        response_serializer = OrderResponseSerializer(instance)
        return response_serializer.data
