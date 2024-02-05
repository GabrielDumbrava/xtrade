"""Application configuration for customusers app."""

from django.apps import AppConfig


class CustomusersConfig(AppConfig):
    """Application configuration"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "customusers"
    verbose_name = "Authentication and Authorization"
