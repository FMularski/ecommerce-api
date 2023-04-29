from django.urls import path

from .views import ProductCategoryListView

urlpatterns = [
    path("categories/", ProductCategoryListView.as_view(), name="categories"),
]
