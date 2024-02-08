"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application  # type: ignore
from dotenv import load_dotenv
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
DOTENV_FILE = APP_ROOT / ".env"
load_dotenv(DOTENV_FILE)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

application = get_wsgi_application()
