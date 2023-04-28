from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import Order, OrderItem, Product, ProductCategory, ShippingAddress


class ShippingAddressAdmin(ModelAdmin):
    list_display = "user", "full_name", "street", "city", "zip_code", "country"
    search_fields = (
        "user",
        "full_name",
        "street",
    )
    list_filter = ("country",)


class ProductCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
    )
    list_filter = ("category",)
    search_fields = ("name",)


class OrderItemInline(TabularInline):
    model = OrderItem
    fields = "product", "quantity"
    extra = 0


class OrderAdmin(ModelAdmin):
    list_display = (
        "pk",
        "user",
        "created_at",
        "payment_deadline",
        "total_price",
    )
    list_filter = ("user",)
    search_fields = ("user",)
    readonly_fields = ("created_at",)
    inlines = (OrderItemInline,)


admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
