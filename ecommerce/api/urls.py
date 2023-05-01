from django.urls import path

from .views import OrderListView, ProductDetailView, ProductListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("product/<pk>/", ProductDetailView.as_view(), name="product"),
    path("orders/", OrderListView.as_view(), name="orders"),
]
