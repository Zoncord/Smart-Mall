from django.conf import UserSettingsHolder
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class ExtendedUserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "email",
        "mobile_number",
    )
    list_filter = ("is_staff",)
    # add_form = CustomUserCreationForm
    ordering = ("email",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "avatar",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "mobile_number",
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
                    # "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
