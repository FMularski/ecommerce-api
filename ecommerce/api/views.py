from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from ecommerce.models import Product, ProductCategory

from .pagination import ProductPagination
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @swagger_auto_schema(
        operation_description="Returns the list of products.",
        manual_parameters=[
            openapi.Parameter(
                "order",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["name", "category", "price"],
            ),
            openapi.Parameter("name", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=list(ProductCategory.objects.all().values_list("name", flat=True)),
            ),
            openapi.Parameter("desc", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter("price", openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        products = Product.objects.all().order_by("pk")

        # apply filters
        name = self.request.GET.get("name")
        category = self.request.GET.get("category")
        description = self.request.GET.get("desc")
        price = self.request.GET.get("price")

        if name:
            products = products.filter(name__icontains=name)
        if category:
            products = products.filter(category__name__iexact=category)
        if description:
            products = products.filter(description__icontains=description)
        if price:
            products = products.filter(price=price)

        # apply ordering
        order_by = self.request.GET.get("order")

        if order_by:
            products = products.order_by(order_by)

        return products
