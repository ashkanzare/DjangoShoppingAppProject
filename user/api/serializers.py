from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'phone', 'is_staff', 'is_customer']


class CustomerUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'phone', 'is_customer']
