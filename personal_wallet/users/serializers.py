from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


ACCESS_TOKEN_RESPONSE_KEY = 'access_token'
REFRESH_TOKEN_RESPONSE_KEY = 'refresh_token'
MSG_USERNAME_ALREADY_EXIST = 'A user with this username address already exists.'
MSG_INCORRECT_CREDENTIALS = 'Incorrect credentials.'
MSG_USERNAME_AND_PASSWORD_NEEDED = 'Username and password needed.'

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(MSG_USERNAME_ALREADY_EXIST)
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = self.get_token(user)
                attrs[REFRESH_TOKEN_RESPONSE_KEY] = str(refresh)
                attrs[ACCESS_TOKEN_RESPONSE_KEY] = str(refresh.access_token)
            else:
                msg = MSG_INCORRECT_CREDENTIALS
                raise serializers.ValidationError(msg)
        else:
            msg = MSG_USERNAME_AND_PASSWORD_NEEDED
            raise serializers.ValidationError(msg)

        return attrs

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return refresh
