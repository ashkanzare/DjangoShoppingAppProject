from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import datetime

from constants import vars as const
from customer.models import Customer
from product.models import Product, ProductFactorProperty, ProductColor


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=const.CUSTOMER, blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True, default=None)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=const.CART_STATUS, verbose_name=const.STATUS, default=const.ACTIVE)

    def __str__(self):
        return f"[ {self.customer.id} ] -- [ {self.customer.user.phone} ] -- [ {self.creation_date} ]"

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
        cart_items = self.cartitem_set.all()
        if cart_items:
            for item in cart_items:
                item_price = item.product.calc_price_base_of_color_and_factor_property(
                    item.product_property.id if item.product_property else None,
                    item.product_color.id if item.product_color else None)
                if isinstance(item_price, tuple):
                    total_price += item_price[0] * item.number
                else:
                    total_price += item_price * item.number

                total_price_with_discount += item.product.calc_final_price_with_properties(
                    item.product_property.id if item.product_property else None,
                    item.product_color.id if item.product_color else None)[0] * item.number

            discount = total_price - total_price_with_discount
            discount_percentage = round(100 - (100 * total_price_with_discount / total_price), 2)

            return total_price, total_price_with_discount, discount_percentage, discount
        return 0


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


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=const.CART)
    status = models.CharField(max_length=100, choices=const.ORDER_STATUS)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[ {self.cart.id} ] -- [ {self.status} ] -- [ {self.date} ]"
