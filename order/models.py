from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.datetime_safe import datetime

from constants import vars as const
from customer.models import Customer, Address, MeCoinWallet
from product.models import Product, ProductFactorProperty, ProductColor
from utils.utils_functions import send_processing_sms_thread


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=const.CUSTOMER, blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True, default=None)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=const.CART_STATUS, verbose_name=const.STATUS, default=const.ACTIVE)

    def __str__(self):
        return f"[ {self.customer.id if self.customer else self.session} ] -- " \
               f"[ {self.customer.user.phone if self.customer else self.session} ] -- [ {self.creation_date} ]"

    def check_date(self):
        current_date = datetime.now()
        time_diff = current_date - self.creation_date
        return time_diff.seconds / 3600 < 3

    def add_item(self, product, product_color, product_property, number):
        try:
            cart_item = CartItem.objects.get(cart=self, product_id=product, product_color_id=product_color,
                                             product_property_id=product_property)

            quantity_check, quantity_number = cart_item.check_product_with_properties_exist()

            cart_item.number += number
            if number > 0:
                if quantity_check and cart_item.number <= quantity_number:
                    cart_item.save()
                    return True, 'added'

            elif cart_item.number > 0:

                cart_item.save()
                return True, 'deleted-one'

            elif cart_item.number == 0:
                cart_item.delete()
                return True, 'deleted'

            return False, None

        except CartItem.DoesNotExist:
            cart_item = CartItem(cart=self, product_id=product, product_color_id=product_color,
                                 product_property_id=product_property, number=number)

            quantity_check, quantity_number = cart_item.check_product_with_properties_exist()

            if quantity_check and cart_item.number <= quantity_number:
                cart_item.save()
                return True, None

            return False, None

    @classmethod
    def get_or_none(cls, user):
        cart = None
        try:
            cart = Cart.objects.get(customer__user=user, status='active')
        except Cart.DoesNotExist:
            pass
        finally:
            return cart

    @classmethod
    def get_by_session_or_none(cls, session):
        cart = None
        try:
            cart = Cart.objects.get(session=session, status='active')
        except Cart.DoesNotExist:
            pass
        finally:
            return cart

    def calc_price(self):
        total_price = 0
        total_price_with_discount = 0
        discount = 0
        discount_percentage = 0

        cart_items = self.cartitem_set.all()
        if cart_items:
            for item in cart_items:
                item_price = item.get_item_price()
                total_price += item_price[2] * item.number
                total_price_with_discount += item_price[0] * item.number
            discount = total_price - total_price_with_discount
            discount_percentage = round(100 - (100 * total_price_with_discount / total_price), 2)

        return total_price, total_price_with_discount, discount_percentage, discount

    def merge_with_session(self, other):
        for item in other.cartitem_set.all():
            self.add_item(item.product.id, item.product_color.id if item.product_color else None,
                          item.product_property.id if item.product_property else None, item.number)

    @classmethod
    def sync_cart_from_session(cls, session, user):
        cart_by_session = Cart.get_by_session_or_none(session)
        cart_by_customer = Cart.get_or_none(user)

        if (cart_by_session and cart_by_customer) and (cart_by_session != cart_by_customer):
            cart_by_customer.merge_with_session(cart_by_session)
            cart_by_session.delete()

        elif cart_by_session and not cart_by_customer:
            cart = cart_by_session
            cart.customer = Customer.objects.get(user=user)
            cart.session = None
            cart.save()

    def cart_mecoin(self):
        price_amount = self.calc_price()[1] / const.PRODUCT_MECOIN_UNIT
        return MeCoinWallet.convert_to_mecoin(price_amount)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=const.CART)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=const.PRODUCT)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, verbose_name=const.COLOR, null=True,
                                      blank=True)
    product_property = models.ForeignKey(ProductFactorProperty, on_delete=models.CASCADE, verbose_name=const.PROPERTY,
                                         null=True, blank=True)
    number = models.PositiveIntegerField(verbose_name=const.NUMBER)

    def __str__(self):
        return f"[ {self.product.name} ] -- [ {self.number} ]"

    is_cleaned = True

    def clean(self):
        if self.product_property:
            if self.product != self.product_property.product:
                self.is_cleaned = False
        if self.product_color:
            if self.product != self.product_color.product:
                self.is_cleaned = False
        if not self.is_cleaned:
            raise ValidationError(const.ADD_PRODUCT_ERROR, code='invalid')

    def save(self, *args, **kwargs):
        if self.is_cleaned:
            self.clean()

        super().save(*args, **kwargs)

    def check_product_with_properties_exist(self):
        property_set = self.product.productfactorproperty_set
        color_set = self.product.productcolor_set

        product_color = self.product_color
        product_property = self.product_property

        filtered_color_set = color_set.filter(pk=product_color.id if product_color else None)
        filtered_property_set = property_set.filter(pk=product_property.id if product_property else None)

        color_set_len = 0
        property_set_len = 0

        if filtered_color_set:
            color_set_len = filtered_color_set[0].quantity

        if filtered_property_set:
            property_set_len = filtered_property_set[0].quantity

        if product_color and product_property:
            if filtered_color_set and filtered_property_set:
                return True, color_set_len if color_set_len >= property_set_len else property_set_len
            return False, 0

        elif product_color or self.product_property:
            if filtered_color_set or filtered_property_set:
                return True, color_set_len if color_set_len >= property_set_len else property_set_len
            return False, 0

        elif self.product.quantity != 0:
            return True, self.product.quantity

        else:
            return False, 0

    def get_item_price(self):
        color_id = self.product_color.id if self.product_color else None
        property_id = self.product_property.id if self.product_property else None

        price_set = self.product.calc_final_price_with_properties(property_id, color_id)
        return price_set


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name=const.CART)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, verbose_name=const.ADDRESS)
    status = models.CharField(max_length=100, choices=const.ORDER_STATUS_CHOICES, verbose_name=const.ORDER_STATUS,
                              default=const.INITIAL)
    shipping_type = models.CharField(max_length=50, choices=const.SHIPPING_TYPE_CHOICES,
                                     verbose_name=const.SHIPPING_TYPE)
    customer_discount = models.FloatField(default=0)
    payment_method = models.CharField(max_length=100, choices=const.ORDER_PAYMENT_CHOICES,
                                      verbose_name=const.PAYMENT_METHOD, default=const.ONLINE)
    date = models.DateTimeField(auto_now=True, verbose_name=const.DATE)

    def __str__(self):
        return f"[ {self.cart.id} ] -- [ {self.status} ] -- [ {self.date} ] -- [ {self.payment_method} ]"

    @property
    def total_cart_price_info(self):
        cart_price = self.cart.calc_price()
        return cart_price

    @property
    def total_cart_price(self):
        cart_price = self.cart.calc_price()[1]
        customer_discount = self.customer_discount

        if customer_discount == 0:
            return cart_price

        return cart_price * (1 - customer_discount / 100)

    @property
    def total_price(self):
        cart_price = self.total_cart_price
        if cart_price >= const.FREE_SHIPPING_MIN_PRICE:
            return cart_price
        return cart_price + const.SHIPPING_TYPE_TO_PRICE[self.shipping_type]

    @property
    def pay_amount(self):
        if self.status == const.WAITING_FOR_PAY or self.payment_method == const.CASH_ON_DELIVERY:
            return self.total_price
        return 0

    @property
    def order_number(self):
        return 'MESH' + f"{hash(self.date.strftime('%Y-%m-%d') + str(self.id))}"[1:6]

    @property
    def order_code(self):
        return f"{hash(self.date.strftime('%Y-%m-%d') + str(self.id))}"[-5:]

    def save(self, *args, **kwargs):
        if self.status == const.WAITING_FOR_PAY or self.status == const.PROCESSING:
            self.cart.status = 'inactive'
            self.cart.save()
        if self.status == const.PROCESSING:
            send_processing_sms_thread(
                {'name': self.cart.customer.first_name,
                 'order': self.order_number,
                 'code': self.order_code,
                 'link': reverse('order:order-detail', args=[self.id])},
                [f'98{self.cart.customer.user.phone}']
            )

        super().save(*args, **kwargs)

    @classmethod
    def get_by_user(cls, user):
        order = None
        try:
            order = cls.objects.get(cart__customer__user=user)
        except cls.DoesNotExist:
            pass
        return order

    @classmethod
    def get_or_none(cls, order_id):
        order = None
        try:
            order = cls.objects.get(pk=order_id)
        except cls.DoesNotExist:
            pass
        return order

    @property
    def has_free_shipping(self):
        cart_price = self.total_cart_price
        return cart_price >= const.FREE_SHIPPING_MIN_PRICE, const.SHIPPING_TYPE_TO_PRICE[self.shipping_type]
