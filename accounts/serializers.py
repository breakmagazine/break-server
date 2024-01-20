from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh_token'])
        data = {'access_token': str(refresh.access_token)}

        return data

class UserRegisterSerializer(DefaultRegisterSerializer):
    # name = serializers.CharField(max_length=50, write_only=True, required=True)
    def custom_signup(self, request, user):
        print(self.validated_data)
        # if name:
        #     user.name = name
        #     user.save()