from django import template
import jdatetime
from datetime import datetime
import webcolors

import constants.vars as const
from product.models import ProductDiscount
from customer.models import MeCoinWallet

register = template.Library()


@register.filter(name='en_to_fa')
def en_to_fa(text):
    """convert english number to persian"""
    fa_numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    text_list = list(str(text))
    for i in range(len(text_list)):
        if text_list[i].isnumeric():
            text_list[i] = fa_numbers[int(text_list[i])]
    return ''.join(text_list)


@register.filter(name='price_format')
def price_format(price):
    print(price)
    int_price = format(int(price), ',')
    return en_to_fa(str(int_price))


@register.filter(name='mecoin')
def mecoin(price):
    mecoin_amount = MeCoinWallet.convert_to_mecoin(price / const.PRODUCT_MECOIN_UNIT)
    int_price = format(mecoin_amount, ',')
    return en_to_fa(str(int_price))


@register.filter(name='list_range')
def list_range(list_obj, range_str):
    start, end = range_str.split('-')
    if start == '':
        return list_obj[:int(end)]
    elif end == '':
        return list_obj[int(start):]
    return list_obj[int(start):int(end)]


@register.filter(name='short_description')
def short_description(text):
    if len(text) > 40:
        return f'{text[:40]}...'
    return text


@register.filter(name='date_delta')
def date_delta(date_time):
    """ compute delta time between now and post date """
    now = datetime.now()
    delta = now - date_time
    if delta.days != 0:
        days = delta.days, 'روز'
        if days[0] >= 30:
            days = int(days[0] / 30), 'ماه'
        return f"{en_to_fa(days[0])} {days[1]}"

    elif delta.seconds != 0:
        seconds = delta.seconds, 'ثانیه'
        if seconds[0] >= 3600:
            seconds = int(seconds[0] / 3600), 'ساعت'
        elif seconds[0] >= 60:
            seconds = int(seconds[0] / 60), 'دقیقه'
        return f"{en_to_fa(seconds[0])} {seconds[1]}"


@register.filter(name='convert_date')
def convert_date(date):
    """ get christian year and convert to jalali date """
    if date:
        j_date = jdatetime.date.fromgregorian(day=date.day, month=date.month, year=date.year)
        month = j_date.j_months_fa[j_date.month - 1]
        return f"{en_to_fa(j_date.day)} {month} {en_to_fa(j_date.year)}"
    return None


@register.filter(name='return_full_name')
def return_full_name(customer_obj):
    """ return fullname of a customer """
    return f"{customer_obj.first_name if customer_obj.first_name else ''}" \
           f" {customer_obj.last_name if customer_obj.last_name else ''}" if (
            customer_obj.first_name or customer_obj.last_name) else '-'


@register.filter(name='return_empty_if_none')
def return_empty_if_none(obj):
    """ return - if obj is none """
    return f"{obj}" if obj else '-'


@register.filter(name='return_empty_str_if_none')
def return_empty_str_if_none(obj):
    """ return '' if obj is none """
    return f"{obj}" if obj else ''


@register.filter(name='get_fullname_or_return_phone')
def get_fullname_or_return_phone(customer_obj):
    """ return fullname of a customer if exists or their phone """
    if customer_obj.first_name and customer_obj.last_name:
        return f"{customer_obj.first_name} {customer_obj.last_name}"
    return f"۰{en_to_fa(customer_obj.user.phone)}"


@register.filter(name='month_number_to_name')
def month_number_to_name(number):
    """ convert month's number to it's name """
    return jdatetime.datetime.j_months_fa[number - 1]


@register.filter(name='get_price_by_factor_property')
def get_price_by_factor_property(product_obj, property_id):
    factor_price = product_obj.productfactorproperty_set.get(pk=property_id).price_impact
    return product_obj.price + factor_price


@register.filter(name='get_final_price_for_a_product')
def get_final_price_for_a_product(price, product_id):
    product_discount = ProductDiscount.get_or_none(product_id)
    if product_discount:
        return price - product_discount.discount_amount * price / 100
    return price


@register.filter(name='convert_hex_to_name')
def convert_hex_to_name(color_hex):
    return webcolors.hex_to_name(str(color_hex))


@register.filter(name='subtract')
def subtract(num_1, num_2):
    return num_1 - num_2


@register.filter(name='add')
def add(num_1, num_2):
    return num_1 + num_2


@register.filter(name='multiply')
def multiply(num_1, num_2):
    return float(num_1) * float(num_2)


@register.filter(name='str_split')
def str_split(string, separator_index):
    separator, index = separator_index.split('-')
    return string.split(separator)[int(index)]


@register.filter(name='shipping_type_convert')
def shipping_type_convert(string):
    return "ارسال توسط میشاپ" if string == 'MESHOP' else "ارسال توسط پست"


@register.filter(name='find_discount')
def find_discount(price, percent):
    return price * (1 - percent / 100)
