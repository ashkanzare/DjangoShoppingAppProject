from django.contrib.auth.models import AbstractUser
from django.db import models


from constants.vars import *

from user.models import User
from utils.utils_functions import generate_random_string, validate_discount_date

""" Customer App's Models """


class Customer(models.Model):
    """
     Customer Model contains:
            user(required),
            first_name(optional),
            last_name(optional),
            birthday(optional),
            personal_id(optional),
            email(optional)
     """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=USERNAME)
    first_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=FIRST_NAME)
    last_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=LAST_NAME)
    birthday = models.DateField(blank=True, null=True, verbose_name=BIRTHDAY)
    personal_id = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name=PERSONAL_ID)
    email = models.EmailField(blank=True, null=True, verbose_name=EMAIL)

    def __str__(self):
        return f'{self.user.phone} -- {self.last_name if self.last_name else NO_NAME}'


class Address(models.Model):
    """
    Address Model contains:
            customer(required),
            address(required)
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=CUSTOMER)
    address = models.TextField(verbose_name=ADDRESS)

    def __str__(self):
        return f"{self.customer} -- {self.address[:25]}..."


class DiscountCode(models.Model):
    """
    DiscountCode Model contains:
            customer(required),
            discount_code(required)
   """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=CUSTOMER,
                                 help_text=SEARCH_FOR_USER_HELP_TEXT)
    discount_code = models.CharField(max_length=8, default=generate_random_string, verbose_name=DISCOUNT_CODE)
    end_date = models.DateTimeField(default=validate_discount_date, verbose_name=END_DATE, help_text=END_DATE_HELP_TEXT)

    def __str__(self):
        return f"{self.customer.user.phone} -- {self.discount_code}"
