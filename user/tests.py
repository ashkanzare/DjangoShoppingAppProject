from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import time

from user.models import User, UserAuthCode


class ViewTestCase(TestCase):

    def setUp(self):
        # create a user
        User.objects.create_user(phone="9362990885")

    def test_user_auth_code_exp_time(self):
        """
        test auth code expire time

        """
        user = User.objects.get(pk=1)
        code = UserAuthCode.objects.get(user=user)
        # before 2 minutes
        self.assertTrue(code.check_expire_time())
        # after 2 minutes
        # time.sleep(121)
        # self.assertTrue(code.check_expire_time())

