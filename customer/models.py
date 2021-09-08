from django.contrib.auth.models import AbstractUser
from django.db import models
from constants.vars import *

# Create your models here.
from user.models import User
from utils.utils_functions import generate_random_string


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=USERNAME)
    first_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=FIRST_NAME)
    last_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=LAST_NAME)
    birthday = models.DateField(blank=True, null=True, verbose_name=BIRTHDAY)
    personal_id = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name=PERSONAL_ID)
    email = models.EmailField(blank=True, null=True, verbose_name=EMAIL)

    def __str__(self):
        return f'{self.user.phone} -- {self.last_name if self.last_name else NO_NAME}'


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=CUSTOMER)
    address = models.TextField(verbose_name=ADDRESS)

    def __str__(self):
        return f"{self.customer} -- {self.address[:25]}..."


class DiscountCode(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=CUSTOMER)
    discount_code = models.CharField(max_length=8, default=generate_random_string)


