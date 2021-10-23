import re

from django.contrib.auth import login, authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customer.models import Customer
from user.api.serializers import UserSerializer, CustomerUserSerializer, UserAuthCodeSerializer, \
    UserPasswordSerializer, ResetPasswordSerializer
from user.models import User, UserAuthCode
from utils.utils_functions import send_email_thread, send_sms_thread


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_customer=True)
    serializer_class = CustomerUserSerializer

    def create(self, request, *args, **kwargs):
        user, created = User.objects.get_or_create(phone=request.data['phone'])
        if created:
            user.is_customer = True
            user.save()
            auth_code = UserAuthCode.objects.create(user=user)
            return Response({'code': auth_code.code})


@api_view(['POST', ])
def register_login_view(request):
    if request.method == 'POST':
        serializer = CustomerUserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            # user does not exist -> register
            phone_or_email = request.data['phone']
            if re.search(r'^9\d{9}$', phone_or_email):
                user = serializer.save()
                Customer.objects.create(user=user)
                user.is_customer = True
                user.is_active = False
                user.save()
                data = {
                    'response': 'user created successfully',
                    'phone': user.phone,
                    'token': Token.objects.get(user=user).key,
                    'active': user.is_active,
                    'status': 1
                }
                send_sms_thread(
                    str(UserAuthCode.objects.get(user=user).code),
                    [f'+98{user.phone}'],
                )
            elif re.search(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', phone_or_email):
                user_with_given_email = User.objects.filter(email__iexact=phone_or_email)
                if user_with_given_email:
                    user = user_with_given_email[0]
                    data = {
                        'response': 'user exists',
                        'token': Token.objects.get(user=user).key,
                        'status': 3
                    }
                else:
                    data = {
                        'response': 'user does not exist exists',
                        'status': 4
                    }
            else:
                data = {
                    'response': 'invalid input',
                    'status': 5
                }

        else:
            try:
                user = User.objects.get(phone=request.data['phone'])
                # user exists -> login
                data = {
                    'response': 'user exists',
                    'phone': request.data['phone'],
                    'token': Token.objects.get(user=user).key,
                    'status': 0
                }

                send_sms_thread(
                    str(UserAuthCode.create_or_get_and_delete(user).code),
                    [f'+98{request.data["phone"]}'],
                )
            except User.DoesNotExist:
                data = {
                    'error': serializer.errors,
                    status: 2
                }
        return Response(data)


@api_view(['POST', ])
def check_user_code(request):
    if request.method == 'POST':
        serializer = UserAuthCodeSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                token = Token.objects.get(key=request.data['token'])
                user = token.user
                user_code = UserAuthCode.objects.get(user=user)
                if user_code.check_expire_time():
                    if user_code.code == request.data['code']:
                        data['status'] = 'ok', 10
                        data['active'] = user.is_active = True
                        user.save()
                        login(request, user)
                        user_code.delete()
                        token.delete()
                        Token.objects.create(user=user)

                    else:
                        data['status'] = 'invalid code', 20
                else:
                    new_code = UserAuthCode.create_or_get_and_delete(user=user)
                    data['status'] = 'time is up', 30
                    send_sms_thread(
                        str(new_code.code),
                        [f'+98{new_code.user.phone}'],
                    )
            except (UserAuthCode.DoesNotExist, Token.DoesNotExist):
                data['status'] = 'invalid input', 40
        else:
            data['error'] = serializer.errors
        return Response(data)


@api_view(['POST', ])
def refresh_code(request):
    if request.method == 'POST':
        serializer = UserAuthCodeSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                token = Token.objects.get(key=request.data['token'])
                user = token.user

                new_code = UserAuthCode.create_or_get_and_delete(user=user)
                data['status'] = 'ok', 20
                send_sms_thread(
                    str(new_code.code),
                    [f'+98{new_code.user.phone}'],
                )

            except (UserAuthCode.DoesNotExist, Token.DoesNotExist):
                data['status'] = 'invalid input', 40

        else:
            data['error'] = serializer.errors
            return Response(data)
        return Response(data)


@api_view(['POST', ])
def login_with_password(request):
    if request.method == 'POST':
        serializer = UserPasswordSerializer(data=request.data)
        data = {}
        user = None
        if serializer.is_valid():
            try:
                token = Token.objects.get(key=request.data['token'])
                user = token.user
                UserAuthCode.objects.get(user=user).delete()

            except (UserAuthCode.DoesNotExist, Token.DoesNotExist):
                data['status'] = 'invalid input', 40

            finally:
                authed_user = authenticate(phone=user.phone, password=request.data['password'])
                if authed_user:
                    login(request, user)
                    data['status'] = 'login successfully', 20
                else:
                    data['status'] = 'login failed', 50

        else:
            data['error'] = serializer.errors
            return Response(data)
        return Response(data)


@api_view(['POST', ])
def reset_password_get_code(request):
    if request.method == 'POST':
        data = {}
        serializer = CustomerUserSerializer(data=request.data)

        if not serializer.is_valid() or serializer.is_valid():

            phone_or_email = request.data['phone']

            if re.search(r'^9\d{9}$', phone_or_email):

                try:
                    user = User.objects.get(phone=phone_or_email)
                    # user exists -> login
                    data = {
                        'response': 'user exists',
                        'phone': request.data['phone'],
                        'token': Token.objects.get(user=user).key,
                        'status': 0
                    }
                    send_sms_thread(
                        str(UserAuthCode.create_or_get_and_delete(user).code),
                        [f'+98{phone_or_email}'],
                    )
                except User.DoesNotExist:
                    data = {
                        'error': serializer.errors,
                        status: 2
                    }
            elif re.search(r'^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$', phone_or_email):

                user = User.get_or_none(phone_or_email)
                if user:
                    token = Token.objects.get(user=user).key
                    data = {
                        'response': 'user exists',
                        'email': phone_or_email,
                        'token': token,
                        'status': 3
                    }
                    send_email_thread(
                        'بازیابی رمزعبور',
                        f'به این لینک مراجعه کنید:\n http://127.0.0.1:8000/customer/reset-password/confirm?token={token} ',
                        [phone_or_email], )
                else:
                    data = {
                        'response': 'invalid email',
                        'status': 4
                    }
            else:
                data = {
                    'response': 'invalid input',
                    'status': 5
                }
        return Response(data)


@api_view(['POST', ])
def check_code_for_reset_password(request):
    if request.method == 'POST':
        serializer = UserAuthCodeSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                token = Token.objects.get(key=request.data['token'])
                user = token.user
                user_code = UserAuthCode.objects.get(user=user)

                if user_code.check_expire_time():

                    if user_code.code == request.data['code']:
                        data['status'] = 'ok', 10
                        token.delete()
                        new_token = Token.objects.create(user=user)
                        data = {
                            'status': ['ok', 10],
                            'token': new_token.key}
                    else:
                        data['status'] = 'invalid code', 20
                else:
                    user_code.delete()
                    new_code = UserAuthCode.objects.create(user=user)
                    data['status'] = 'time is up', 30
                    send_sms_thread(
                        str(new_code.code),
                        [f'+98{new_code.user.phone}'],
                    )
            except (UserAuthCode.DoesNotExist, Token.DoesNotExist):
                data['status'] = 'invalid input', 40
        else:
            data['error'] = serializer.errors
        return Response(data)


@api_view(['POST', ])
def change_password(request):
    if request.method == 'POST':
        serializer = ResetPasswordSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            try:
                token = Token.objects.get(key=request.data['token'])
                user = token.user

                if request.data['password1'] == request.data['password2']:
                    get_user = User.objects.get(id=user.id)
                    get_user.set_password(request.data['password1'])
                    get_user.save()
                    data = {
                        'status': ['ok', 10]
                    }

                else:
                    data = {
                        'status': ['not equal passwords', 20]
                    }
            except Token.DoesNotExist:
                data['status'] = 'invalid input', 30
        else:
            data['error'] = serializer.errors
        return Response(data)
