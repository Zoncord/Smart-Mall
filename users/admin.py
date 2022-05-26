from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import LessorProfile, TenantProfile
from rating.admin import UserRatingInline

User = get_user_model()


@admin.register(User)
class ExtendedUserAdmin(BaseUserAdmin):
    inlines = [UserRatingInline]
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
                )
            },
        ),
        (
            _("Groups"),
            {
                "fields": (
                    "is_lessor",
                    "is_tenant",
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
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )


@admin.register(LessorProfile)
class LessorProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    pass
