from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "email",
                    "role",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "role", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "role", "is_staff")
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "role",
    )
    search_fields = ("email",)
    ordering = ("-pk",)


admin.site.register(User, CustomUserAdmin)
