from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

import constants.vars as const
from utils.utils_functions import generate_random_code


# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """ User model """

    username = None
    email = models.EmailField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^9\d{9}$', message=const.PHONE_HELP_TEXT)
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    password = models.CharField(max_length=1000, blank=True, null=True)

    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return f'[ {self.phone} ]'


class UserAuthCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=const.USER)
    code = models.CharField(max_length=5, default=generate_random_code)

    def __str__(self):
        return f'[ {self.user} ] -- [ {self.code} ]'
