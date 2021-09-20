from random import choices
import string
from django.utils.datetime_safe import datetime, time
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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


def compute_code_expire_time():
    """ generate end_date for auth code for 2 minutes """
    timestamp = datetime.utcnow().timestamp()
    timestamp += 120
    return timestamp


def check_personal_code_is_valid(code):
    """ check if a personal id is valid or not """

    if len(code) < 8 or len(code) > 10:
        raise ValidationError(
            _('%(value)s is not valid personal code'),
            params={'value': code},
        )

    else:
        if 8 <= len(code) < 10:
            while len(code) < 10:
                code = "0" + code

        code_numbers_sum = 0
        for i in range(len(code) - 1):
            coefficient = 10 - i
            code_numbers_sum += coefficient * int(code[i])

        reminder = code_numbers_sum % 11

        if reminder <= 2:
            if reminder == int(code[-1]):
                return True

        else:
            if 11 - reminder == int(code[-1]):
                return True

        raise ValidationError(
            _('%(value)s is not valid personal code'),
            params={'value': code},
        )
