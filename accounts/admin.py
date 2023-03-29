from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AdminUser
from .models import User


@admin.register(User)
class User(AdminUser):
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("password", )}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", 'current_city', 'phone')}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('first_name', 'last_name', 'email', 'current_city', 'phone', "password1", "password2"),
            },
        ),
    ),
    ordering = ("email",)
    # add_form = AdminAddForm
