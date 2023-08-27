from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegistrationSerializer
from .serializers import CustomTokenObtainPairSerializer

ACCESS_TOKEN_RESPONSE_KEY = 'access_token'
REFRESH_TOKEN_RESPONSE_KEY = 'refresh_token'


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            REFRESH_TOKEN_RESPONSE_KEY: str(refresh),
            ACCESS_TOKEN_RESPONSE_KEY: str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

