from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import django.utils.timezone as current_time
from django.utils.translation import gettext as _

from constants.vars import *

from utils.utils_functions import generate_random_string, validate_discount_date, check_personal_code_is_valid

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
    LANGUAGE_CHOICES = (
        ('en-us', 'English'),
        ('nl', 'Persian'),
    )
    language = models.CharField(default='fa-ir', choices=LANGUAGE_CHOICES, max_length=5)

    def __str__(self):
        return f"{self.user.phone} -- {self.last_name if self.last_name else NO_NAME}"

    @classmethod
    def get_fields(cls):
        return set([f.name for f in cls._meta.get_fields()])

    @classmethod
    def get_by_token(cls, token):
        user = User.get_user_by_token(token)
        customer = None
        if user:
            customer = Customer.objects.get(user=user)
        return customer

    @classmethod
    def get_by_user_or_none(cls, user):
        customer = None
        try:
            customer = cls.objects.get(user=user, user__is_customer=True)
        except cls.DoesNotExist:
            pass
        return customer

    def get_cart(self):
        cart = self.cart_set.filter(status='active')
        return cart[0].cartitem_set.all() if cart else None

    def get_cart_itself(self):
        cart = self.cart_set.filter(status='active')
        return cart[0] if cart else None

    def get_mecoin(self):
        wallet = None
        try:
            wallet = MeCoinWallet.objects.get(customer=self)
        except MeCoinWallet.DoesNotExist:
            pass

        return wallet

    def check_mecoin(self):
        cart = self.get_cart_itself()
        if cart:
            wallet = self.get_mecoin()
            if wallet:
                return wallet.convert_to_toman() >= cart.calc_price()[1]

            return False
        return False

    def use_mecoin(self, price):
        """ use customer wallet for purchase """
        price_per_mecoin = price / MECOIN_PER_TOMAN
        customer_wallet = self.get_mecoin()
        if customer_wallet:
            customer_wallet.coin -= price_per_mecoin
            customer_wallet.save()
        return price_per_mecoin


class Address(models.Model):
    """
    Address Model contains:
            customer(required),
            address(required)
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_(CUSTOMER), null=True, blank=True)
    state = models.CharField(max_length=100, verbose_name=STATE)
    city = models.CharField(max_length=100, verbose_name=CITY)
    postal_address = models.TextField(verbose_name=POSTAL_ADDRESS)

    postal_code_regex = RegexValidator(regex=r'\d{10}', message=POSTAL_CODE_HELP_TEXT)
    postal_code = models.CharField(max_length=10, verbose_name=POSTAL_CODE, validators=[postal_code_regex])

    building_number = models.PositiveIntegerField(verbose_name=BUILDING_NUMBER)
    building_unit = models.CharField(max_length=5, verbose_name=BUILDING_UNIT)

    receiver_first_name = models.CharField(max_length=250, verbose_name=RECEIVER_FIRST_NAME)
    receiver_last_name = models.CharField(max_length=250, verbose_name=RECEIVER_LAST_NAME)

    phone_code_regex = RegexValidator(regex=r'^09\d{9}', message=PHONE_HELP_TEXT)
    receiver_phone = models.CharField(max_length=11, verbose_name=RECEIVER_PHONE, validators=[phone_code_regex])

    position_x = models.FloatField(default=MAP_X)
    position_y = models.FloatField(default=MAP_Y)

    def __str__(self):
        return f"[ {self.customer} ] -- [ {self.state} -- {self.city} ] "


class DiscountCode(models.Model):
    """
    DiscountCode Model contains:
            customer(required),
            discount_code(required)
   """
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name=_(CUSTOMER),
                                    help_text=_(SEARCH_FOR_USER_HELP_TEXT))
    discount_code = models.CharField(max_length=8, default=generate_random_string, verbose_name=_(DISCOUNT_CODE))
    discount_amount = models.FloatField(default=0, verbose_name=_(DISCOUNT))
    end_date = models.DateTimeField(default=validate_discount_date, verbose_name=_(END_DATE),
                                    help_text=_(END_DATE_HELP_TEXT))

    def __str__(self):
        return f"{self.customer.user.phone} -- {self.discount_code} -- {self.discount_amount}%"

    @classmethod
    def get_by_token_and_code(cls, token, code):
        customer = Customer.get_by_token(token)
        discount = None
        if customer:
            discount = cls.objects.filter(customer=customer, discount_code=code)
        if discount:
            discount = discount[0]
        return discount


class MeCoinWallet(models.Model):
    """
        MeCoinWallet Model contains:
                customer(required),
                coin(required)
    """
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name=_(CUSTOMER))
    coin = models.FloatField(default=0, verbose_name=_(COIN))

    def __str__(self):
        return f"{self.customer.user.phone} -- {self.coin} M.C"

    def add_coin(self, coin_amount):
        """ add coin to customer wallet """
        self.coin += coin_amount
        self.save()

    def convert_to_toman(self):
        """ convert MeCoin to Toman """
        return self.coin * MECOIN_PER_TOMAN

    @classmethod
    def convert_to_mecoin(cls, toman_amount):
        """ convert Toman to MeCoin """
        return toman_amount / MECOIN_PER_TOMAN
