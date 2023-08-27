from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from personal_wallet.utils_for_urls import CUSTOM_USER_REGISTRATION_URL_CONSTANT, TOKEN_OBTAIN_URL_CONSTANT, \
                                           TOKEN_REFRESH_URL_CONSTANT
from .views import UserRegistrationView

urlpatterns = [
    path(CUSTOM_USER_REGISTRATION_URL_CONSTANT, UserRegistrationView.as_view()),
    path(TOKEN_OBTAIN_URL_CONSTANT, TokenObtainPairView.as_view()),
    path(TOKEN_REFRESH_URL_CONSTANT, TokenRefreshView.as_view()),
]