"""
URL configuration for buylando project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

description = """
Project created as a recruitment task. API for browsing and managing products and orders.
Objects can be also inspected at http://localhost/admin/, credentials: e: admin@mail.com p: admin

Created by mularskif@gmail.com
"""

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version="v1",
        description=description,
        contact=openapi.Contact(email="mularskif@gmail.com"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
]
