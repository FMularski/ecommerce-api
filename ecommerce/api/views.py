from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from ecommerce.models import ProductCategory

from .serializers import ProductCategorySerializer


class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    @swagger_auto_schema(
        operation_description="Returns the list of products' categories.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
