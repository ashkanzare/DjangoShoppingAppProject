from random import choices
import string

from django.utils.datetime_safe import datetime

"""
    utils_function.py is a module for extra functions that project needed

"""


def generate_random_string():
    """ generate random string with length 8 for discount code """
    chars = string.ascii_uppercase + string.digits
    return ''.join(choices(chars, k=8))


def generate_random_code():
    """ generate random 5 digits number for user auth """
    chars = string.digits
    return ''.join(choices(chars, k=5))


def validate_discount_date():
    """ generate end_date for discount code for 30 days """
    timestamp = datetime.utcnow().timestamp()
    timestamp += 30 * 24 * 3600
    return datetime.fromtimestamp(timestamp)
