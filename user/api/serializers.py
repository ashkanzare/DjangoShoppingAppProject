from rest_framework import serializers

from user.models import User, UserAuthCode
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'phone', 'is_staff', 'is_customer']


class CustomerUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'phone']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class UserAuthCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthCode
        fields = ['code']


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=1000, min_length=6)
    password2 = serializers.CharField(max_length=1000, min_length=6)
