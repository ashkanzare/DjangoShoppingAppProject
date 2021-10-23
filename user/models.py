from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext as _

import constants.vars as const
from utils.utils_functions import generate_random_code, compute_code_expire_time
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        if password:
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

        return self._create_user(phone, password, is_manager=True, **extra_fields)


class User(AbstractUser):
    """ User model """

    username = None
    # phone_regex = RegexValidator(regex=r'^9\d{9}$', message=_(const.PHONE_HELP_TEXT))
    phone = models.CharField(max_length=10000, unique=True, verbose_name=_(const.PHONE))
    is_customer = models.BooleanField(default=False, verbose_name=_(const.CUSTOMER))
    is_manager = models.BooleanField(default=False, verbose_name=_(const.MANAGER))
    is_employee = models.BooleanField(default=False, verbose_name=_(const.STAFF))

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return f'[ {self.phone} ]'

    def check_if_user_has_password(self):
        return True if self.password else False

    def update_by_kwargs(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    def get_token(self):
        try:
            token = Token.objects.get(user=self)
        except Token.DoesNotExist:
            token = ''
        return token

    @classmethod
    def get_user_by_token(cls, token):
        user = None
        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            pass
        return user

    @classmethod
    def get_or_none(cls, email_or_phone):
        user = None
        try:
            if email_or_phone.isnumeric():
                user = User.objects.get(phone__exact=email_or_phone)
            else:
                user = User.objects.get(email__iexact=email_or_phone)
        except User.DoesNotExist:
            pass
        finally:
            return user

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_employee:
            try:
                group = Group.objects.get(name='staff')
                self.groups.add(group)
            except Group.DoesNotExist:
                pass


class UserAuthCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_(const.USER), unique=True)
    code = models.CharField(max_length=5, default=generate_random_code, verbose_name=_(const.USER_AUTH_CODE))
    exp_time = models.IntegerField(default=compute_code_expire_time, verbose_name=_(const.EXP_TIME))

    def __str__(self):
        return f'[ {self.user} ] -- [ {self.code} ]'

    def check_expire_time(self):
        now = int(datetime.utcnow().timestamp()) - 5
        remaining_time = self.exp_time - now
        return 0 < remaining_time <= 125

    @classmethod
    def create_or_get_and_delete(cls, user):
        try:
            old_user_auth_code = cls.objects.get(user=user)
            old_user_auth_code.delete()

        except cls.DoesNotExist:
            pass

        finally:
            new_user_auth_code = cls.objects.create(user=user)
            return new_user_auth_code


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        UserAuthCode.objects.create(user=instance)
        Token.objects.create(user=instance)
