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
from django.contrib import admin
from django.urls import path, include

from .utils_for_urls import ADMIN_URL_CONSTANT, GET_URLS_CONSTANT, CUSTOM_USER_URL_CONSTANT, CUSTOM_USER_APP_NAME, \
                            URLS_FILE_CONSTANT
from .views import get_all_urls

urlpatterns = [
    path(ADMIN_URL_CONSTANT, admin.site.urls),
    path(GET_URLS_CONSTANT, get_all_urls),
    # path(CUSTOM_USER_URL_CONSTANT, include('{}.{}'.format(CUSTOM_USER_APP_NAME, URLS_FILE_CONSTANT))),
]
