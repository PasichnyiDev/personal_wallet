"""personal_wallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .routes_util import routes_util
from .views import get_all_urls
from django.views.generic import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="PersonalWallet API",
        default_version='v1',
        description="Simple API to manage your own wallets.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly, permissions.AllowAny],
    authentication_classes=[]
)

urlpatterns = [
    path('', RedirectView.as_view(url=routes_util.get_urls_url())),
    path(routes_util.admin_url(), admin.site.urls, name=routes_util.admin_url_name()),
    path(routes_util.get_urls_url(), get_all_urls, name=routes_util.get_urls_url_name()),
    path(routes_util.users_base_url(), include(routes_util.get_users_url_file_name())),
    path(routes_util.wallets_base_url(), include(routes_util.get_wallets_url_file_name())),
    path(routes_util.statistics_base_url(), include(routes_util.get_statistics_url_file_name())),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
