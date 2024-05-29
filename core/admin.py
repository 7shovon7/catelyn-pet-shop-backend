from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, _
from .models import Address, Customer, ProductManager, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("full_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_role",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "full_name", "user_role"),
            },
        ),
    )
    
    list_display = ("email", "full_name", "user_role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)
    
    readonly_fields = ("date_joined",)


admin.site.register([Address, ProductManager, Customer])
