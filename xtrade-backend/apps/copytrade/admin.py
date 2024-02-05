"""Admin interface for copytrade."""

from django.contrib import admin
from django.utils.html import format_html

from copytrade.models import LeadTrader


class LeadTraderAdmin(admin.ModelAdmin):
    """Admin class."""

    list_display = (
        "pk",
        "name",
        "original_name",
        "get_profile_url",
        "status_copy",
        "status_mock_copy",
        "status_available",
        "notify_on_availability",
    )
    list_display_links = ["pk", "name"]
    list_editable = ["status_copy", "status_mock_copy", "notify_on_availability"]
    list_filter = [
        "status_copy",
        "status_mock_copy",
        "check_for_updates",
        "notify_on_availability",
    ]
    fieldsets = (
        (None, {"fields": [("exchange", "profile_url")]}),
        (None, {"fields": [("name", "original_name")]}),
        (
            "Copy",
            {
                "fields": [
                    "status_available",
                    "status_copy",
                    "status_mock_copy",
                ]
            },
        ),
        (
            "Notifications",
            {
                "fields": [
                    (
                        "check_for_updates",
                        "notify_on_availability",
                    )
                ]
            },
        ),
        ("Profile", {"fields": ["profile"]}),
    )

    @admin.display(description="Profile")
    def get_profile_url(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            obj.profile_url,
            obj.name,
        )


admin.site.register(LeadTrader, LeadTraderAdmin)
