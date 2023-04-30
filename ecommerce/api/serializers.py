from rest_framework import serializers

from ecommerce.models import Product, ProductCategory


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
