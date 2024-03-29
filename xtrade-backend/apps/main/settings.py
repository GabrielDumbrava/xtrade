"""
Django settings for xtrade project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import dj_database_url
from os import environ
from pathlib import Path

from django.core import exceptions  # type: ignore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR.parent

SITE_NAME = "xTrade"


def get_env_setting(setting):
    """Get the environment setting or return exception"""
    try:
        return environ[setting]
    except KeyError as exc:
        error_msg = f"Set the {setting} env variable"
        raise exceptions.ImproperlyConfigured(error_msg) from exc


def get_bool_from_environment(name, default=False):
    """Get the boolean value from environment variables."""
    return os.getenv(name, default) in ["True", "true", True]


def get_list_from_environment(name, default=None):
    """The default value should be a list."""
    return (
        [item.strip() for item in environ[name].split(",")]
        if name in environ
        else default if default else []
    )


def get_tuple_list_from_environment(name, default=None):
    """
    List elements must be separated by comma, tuple elements separated by |
    Example:
    John Doe|some_email@server.com,Jane Doe|another_email@server.com
    """
    if os.environ.get(name):
        _return = []
        _list = os.environ.get(name)
        for item in _list.split(","):
            val1, val2 = item.split("|")
            _return.append((val1.strip(), val2.strip()))
        return _return
    return default or []


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_setting("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_environment("DEBUG")
DEBUG_TOOLBAR = get_bool_from_environment("DEBUG_TOOLBAR", DEBUG)

ADMINS = get_tuple_list_from_environment("ADMINS")
MANAGERS = get_tuple_list_from_environment("MANAGERS", ADMINS)

ALLOWED_HOSTS: list[str] = get_list_from_environment("ALLOWED_HOSTS", ["localhost"])

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "customusers",
    "xtrade",
    "copytrade",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if "DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=500,
            conn_health_checks=True,
        ),
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("TIME_ZONE", "UTC")

USE_I18N = False  # For this specific project we relly only on English.

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [APP_DIR / "static"]
# It's safer to keep static and media root dirs out of the source code folder.
STATIC_ROOT = APP_DIR.parent.parent / "www/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "customusers.User"

EMAIL_HOST = environ.get("EMAIL_HOST", "")
EMAIL_PORT = environ.get("EMAIL_PORT", 465)
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER", "your_email@example.com")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_SUBJECT_PREFIX = f"[{SITE_NAME}] "
EMAIL_USE_SSL = get_bool_from_environment("EMAIL_USE_SSL", True)
EMAIL_USE_TLS = not EMAIL_USE_SSL
DEFAULT_FROM_EMAIL = environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
SERVER_EMAIL = environ.get("SERVER_EMAIL", EMAIL_HOST_USER)
# For testing purposes
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DJANGO_LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO")

# Only use override values.
# Defaults: https://docs.djangoproject.com/en/5.0/ref/logging/#default-logging-definition
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console_irrespective_of_debug": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "mail_admins_irrespective_of_debug": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "copytrade": {
            "handlers": ["console_irrespective_of_debug"],
            "level": "INFO",
        },
    },
}
