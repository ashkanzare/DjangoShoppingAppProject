import json
import re
from difflib import SequenceMatcher
from random import choices
import string

from hashlib import sha256
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.datetime_safe import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static
from django.core.mail import send_mail
from sms import send_sms

from constants.vars import STATES
import constants.vars as const
import threading
from ippanel import Client
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

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
            _(const.INVALID_PERSONAL_ID),
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


def check_for_dict_values(dic):
    """ check if values of the given dictionary is not empty """
    empty_values = [dic[key] for key in dic if (dic[key].strip() if isinstance(dic[key], str) else dic[key])]
    return True if empty_values else False


def phone_validator(phone):
    """ validate phone number """
    if re.search(r'^9\d{9}$', phone):
        return True
    return False


def email_validator(email):
    """ validate email """
    if re.search(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', email):
        return True
    return False


def date_validator(date_string):
    """ validate date """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return date_string
    except ValueError:
        raise ValidationError(_('Invalid value: %s') % date_string)


def unique_phone_email_validator(phone_email):
    """ validate uniqueness of email and phone """
    User = get_user_model()
    try:
        User.objects.get(Q(email=phone_email) | Q(phone=phone_email))
        raise ValidationError(_(f'این  {"شماره" if phone_email.isnumeric() else "ایمیل"} در سیستم موجود است'))
    except User.DoesNotExist:
        return phone_email


def get_static(path):
    """ get static files path in views """
    if settings.DEBUG:
        return find(path)
    else:
        return static(path)


def get_states_and_cities(state_name):
    url = get_static('json/iran-states-and-cities-json/iran_cities_with_coordinates.json')
    with open(url, 'r', encoding="utf-8") as jsonfile:
        states = json.load(jsonfile)
        if state_name in STATES:
            index = STATES[state_name]
            return {'cities': [city['name'] for city in states[index]['cities']]}
        return {'cities': 'not found'}


def image_path_generator(instance, filename):
    name = filename.split('.')
    return f"product_{instance.product.id}/{sha256(name[0].encode()).hexdigest()}.{name[-1]}"


def convert_place_name_to_persian(name, is_city=False):
    if is_city:
        url = get_static('json/province-cities/cities.json')
    else:
        url = get_static('json/province-cities/province.json')

    with open(url, 'r', encoding="utf-8") as jsonfile:
        places = json.load(jsonfile)
        place = {place['title']: SequenceMatcher(None, place['slug'].strip().lower(), name.strip().lower()).ratio() for
                 place in places if
                 SequenceMatcher(None, place['slug'].strip().lower(), name.strip().lower()).ratio() > 0.3}
        if place:
            return max(place, key=place.get)
        return None


class EmailThread(threading.Thread):
    def __init__(self, subject, content, recipient_list):
        self.subject = subject
        self.content = content
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self) -> None:
        send_mail(
            self.subject,
            self.content,
            env('SITE_EMAIL'),
            self.recipient_list,
            fail_silently=False
        )


def send_email_thread(subject, content, recipient_list):
    EmailThread(subject, content, recipient_list).start()


class SMSThread(threading.Thread):
    def __init__(self, content, recipient_list):
        self.content = content
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self) -> None:
        # if you want to use faraz sms api just un-comment 203-213 and comment 214-219
        # sms = Client(env('SMS_API_TOKEN'))
        # pattern_values = {
        #     "verification-code": self.content,
        # }
        #
        # sms.send_pattern(
        #     env('SMS_PATTERN'),
        #     env('SMS_NUMBER'),
        #     self.recipient_list[0],
        #     pattern_values,
        # )
        send_sms(
            self.content,
            '+981000',
            self.recipient_list,
            fail_silently=False
        )


def send_sms_thread(content, recipient_list):
    SMSThread(content, recipient_list).start()


class ProcessingSMSThread(threading.Thread):
    def __init__(self, content, recipient_list):
        self.content = content
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self) -> None:
        # if you want to use faraz sms api just un-comment 233-247 and comment 247-252
        # sms = Client(env('SMS_API_TOKEN'))
        # pattern_values = {
        #     "name": self.content['name'],
        #     'order-number': self.content['order'],
        #     'delivery-code': self.content['code'],
        #     'link': self.content['link']
        # }
        #
        # sms.send_pattern(
        #     env('SMS_PATTERN_2'),
        #     env('SMS_NUMBER'),
        #     self.recipient_list[0],
        #     pattern_values,
        # )
        send_sms(
            const.order_sms(self.content),
            '+981000',
            self.recipient_list,
            fail_silently=False
        )


def send_processing_sms_thread(content, recipient_list):
    ProcessingSMSThread(content, recipient_list).start()
