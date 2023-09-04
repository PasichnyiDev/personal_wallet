from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from personal_wallet.routes_util import routes_util
from .views import UserRegistrationView

urlpatterns = [
    path(
        route=routes_util.users_registration_url(for_frontend=False),
        view=UserRegistrationView.as_view(),
        name=routes_util.users_registration_url_name()
    ),
    path(
        route=routes_util.users_obtain_token_url(for_frontend=False),
        view=TokenObtainPairView.as_view(),
        name=routes_util.users_obtain_token_url_name()
    ),
    path(
        route=routes_util.users_refresh_token_url(for_frontend=False),
        view=TokenRefreshView.as_view(),
        name=routes_util.users_refresh_token_url_name()
    ),
]
