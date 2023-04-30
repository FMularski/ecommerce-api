from django.db.utils import ProgrammingError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, parsers, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.api.permissions import IsSeller
from ecommerce.models import Product, ProductCategory

from .pagination import ProductPagination
from .serializers import ProductSerializer, ReadonlyProductSerializer


def _get_categories_enum():
    """
    Method defining enum of products' categories.
    It is needed when the enum is needed and the databases is
    not migrated yet.

    Returns a tuple of lists: names (str) and ids (int)
    """
    try:
        categories = ProductCategory.objects.all()
        enum_str, enum_int = list(categories.values_list("name", flat=True)), list(
            categories.values_list("id", flat=True)
        )
    except ProgrammingError:
        enum_str, enum_int = ["Computers", "Smartphones", "Peripherals", "Consoles"], [
            1,
            2,
            3,
            4,
        ]

    return enum_str, enum_int


class ProductListView(generics.ListCreateAPIView):
    pagination_class = ProductPagination
    parser_classes = [parsers.MultiPartParser]

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
                enum=_get_categories_enum()[0],  # str enum
            ),
            openapi.Parameter("desc", openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter("price", openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Creates a new product.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                default="Bearer <access>",
            ),
            openapi.Parameter(
                "category",
                openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                enum=_get_categories_enum()[1],  # int enum
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductSerializer
        return ReadonlyProductSerializer

    def get_authenticators(self):
        if self.request.method == "POST":
            return [auth() for auth in [JWTAuthentication]]
        return []

    def get_permissions(self):
        if self.request.method == "POST":
            return [permission() for permission in [permissions.IsAuthenticated, IsSeller]]
        return []

    def get_queryset(self):
        if self.request.method == "POST":
            return Product.objects.all()

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


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    parser_classes = [parsers.MultiPartParser]

    @swagger_auto_schema(
        operation_description="Returns the product with the given id.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Deletes the product with the given id.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                default="Bearer <access>",
            ),
            openapi.Parameter(
                "category",
                openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                enum=_get_categories_enum()[1],  # int enum
            ),
        ],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Deletes the product with the given id.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                default="Bearer <access>",
            ),
            openapi.Parameter(
                "category",
                openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                enum=_get_categories_enum()[1],  # int enum
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Deletes the product with the given id.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                default="Bearer <access>",
            ),
        ],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return ProductSerializer
        return ReadonlyProductSerializer

    def get_authenticators(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [auth() for auth in [JWTAuthentication]]
        return []

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permission() for permission in [permissions.IsAuthenticated, IsSeller]]
        return []
