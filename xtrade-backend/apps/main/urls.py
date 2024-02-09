"""
URL configuration for xtrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from os import environ
from django.contrib import admin  # type: ignore
from django.urls import path, include, re_path  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static
from django.views.generic import TemplateView

admin.site.site_header = "xTrade"

ADMIN_URL = environ.get("ADMIN_URL", "admin")

urlpatterns = [
    path(f"{ADMIN_URL}/", admin.site.urls),
    re_path("", TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
