from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import FieldDoesNotExist
from django.db import models
import django.utils.timezone as current_time
from django.utils.translation import gettext as _

from constants.vars import *

from utils.utils_functions import generate_random_string, validate_discount_date, check_personal_code_is_valid, \
    check_for_dict_values

""" Customer App's Models """
User = get_user_model()


class Customer(models.Model):
    """
     Customer Model contains:
            user(required),
            first_name(optional),
            last_name(optional),
            birthday(optional),
            personal_id(optional),
            email(optional),
            date(required)
     """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_(USERNAME))
    first_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(FIRST_NAME))
    last_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=_(LAST_NAME))
    birthday = models.DateField(blank=True, null=True, verbose_name=_(BIRTHDAY))
    personal_id = models.CharField(max_length=200, blank=True, null=True, verbose_name=_(PERSONAL_ID),
                                   validators=[check_personal_code_is_valid])
    # email = models.EmailField(blank=True, null=True, verbose_name=_(EMAIL))
    date = models.DateField(default=current_time.now, verbose_name=_(REGISTER_DATE))

    def __str__(self):
        return f"{self.user.phone} -- {self.last_name if self.last_name else NO_NAME}"

    @classmethod
    def get_fields(cls):
        return set([f.name for f in cls._meta.get_fields()])


class Address(models.Model):
    """
    Address Model contains:
            customer(required),
            address(required)
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_(CUSTOMER))
    MY_CHOICES = (
        ('a', 'Hola'),
        ('b', 'Hello'),
        ('c', 'Bonjour'),
        ('d', 'Boas'),
    )
    choice = models.CharField(max_length=100, choices=MY_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.customer}"


class DiscountCode(models.Model):
    """
    DiscountCode Model contains:
            customer(required),
            discount_code(required)
   """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_(CUSTOMER),
                                 help_text=_(SEARCH_FOR_USER_HELP_TEXT))
    discount_code = models.CharField(max_length=8, default=generate_random_string, verbose_name=_(DISCOUNT_CODE))
    end_date = models.DateTimeField(default=validate_discount_date, verbose_name=_(END_DATE),
                                    help_text=_(END_DATE_HELP_TEXT))

    def __str__(self):
        return f"{self.customer.user.phone} -- {self.discount_code}"
