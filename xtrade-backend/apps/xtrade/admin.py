"""Admin interface for xtrade."""

from django.contrib import admin
from .models import Exchange


class ExchangeAdmin(admin.ModelAdmin):
    """Admin class for Exchange model."""


admin.site.register(Exchange, ExchangeAdmin)
