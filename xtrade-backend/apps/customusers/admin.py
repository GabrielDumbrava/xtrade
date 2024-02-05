"""Admin configuration for our custom users."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from customusers.models import User, GroupProxy
from customusers.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    """Admin class."""

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_superuser", "is_staff", "is_active"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),
        ("Permissions", {"fields": ["is_superuser", "is_staff", "is_active"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["first_name", "email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "first_name"]
    ordering = ["email"]


admin.site.unregister(Group)
admin.site.register(GroupProxy)
admin.site.register(User, UserAdmin)
