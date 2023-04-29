from django.urls import path

from .views import TokenAPIView, TokenRefreshAPIView

urlpatterns = [
    path("token/", TokenAPIView.as_view(), name="token"),
    path("refresh/", TokenRefreshAPIView.as_view(), name="refresh"),
]
