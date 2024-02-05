"""Application configuration for copytrade app."""

from django.apps import AppConfig


class CopytradeConfig(AppConfig):
    """Configuration class for copytrade app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "copytrade"
    verbose_name = "Copy Trade"

    def ready(self):
        # Connect signal handlers. Decorate with @receiver.
        from . import signals  # pylint: disable=import-outside-toplevel, unused-import
