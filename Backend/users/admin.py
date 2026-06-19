from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "role", "organization")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "phone", "role", "organization", "is_active", "is_staff", "is_superuser")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "full_name", "role", "organization", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "full_name", "organization")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")} ),
        ("Personal info", {"fields": ("full_name", "phone", "organization", "role")} ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")} ),
        ("Important dates", {"fields": ("last_login",)} ),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "role", "organization", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )
