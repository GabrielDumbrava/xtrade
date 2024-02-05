"""Application configuration for xtrade app."""

from django.apps import AppConfig


class XtradeConfig(AppConfig):
    """Configuration class for xtrade app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "xtrade"
    verbose_name = "xTrade"
