from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _

from customer.models import Customer, Address, DiscountCode
from user.models import User

import constants.vars as const
from utils.utils_functions import date_validator, unique_phone_email_validator


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class UserPhoneSerializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(regex=r'^9\d{9}$', message=_(const.PHONE_HELP_TEXT))
    phone = serializers.CharField(max_length=10, validators=[phone_regex])

    class Meta:
        model = User
        fields = ['phone']


class CustomerSerializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(regex=r'^9\d{9}$', message=_(const.PHONE_HELP_TEXT))
    phone = serializers.CharField(max_length=10, validators=[phone_regex, unique_phone_email_validator],
                                  allow_null=True, allow_blank=True)
    token = serializers.CharField(max_length=40)
    email = serializers.EmailField(allow_null=True, allow_blank=True, validators=[unique_phone_email_validator])
    birthday = serializers.CharField(allow_null=True, allow_blank=True, validators=[date_validator])

    class Meta:
        model = Customer
        fields = ['token', 'first_name', 'last_name', 'email', 'personal_id', 'birthday', 'phone']


class CreateAddressSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=40)

    class Meta:
        model = Address
        exclude = ['customer']


class UpdateAddressSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=40)
    id = serializers.IntegerField()

    class Meta:
        model = Address
        exclude = ['customer']


class StateCitiesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)


class StateCitiesTranslateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    is_city = serializers.BooleanField(default=False)


class MeCoinConverterSerializer(serializers.Serializer):
    toman_amount = serializers.FloatField()


class CustomerDiscountSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=100, allow_blank=True, required=False)
    order_id = serializers.IntegerField()

    class Meta:
        model = DiscountCode
        fields = ['token', 'order_id', 'discount_code']
