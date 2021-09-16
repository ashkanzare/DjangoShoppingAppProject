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
        extra_kwargs = {
            'description': {'error_messages': {'unique': "shit"}},
        }


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class UserAuthCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthCode
        fields = ['code']
