from django.contrib.auth import login, authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sms import send_sms

from user.api.serializers import UserSerializer, CustomerUserSerializer, UserAuthCodeSerializer, \
    UserPasswordSerializer
from user.models import User, UserAuthCode


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
            user = serializer.save()
            user.is_customer = True
            user.is_active = False
            data = {
                'response': 'user created successfully',
                'phone': user.phone,
                'token': Token.objects.get(user=user).key,
                'active': user.is_active,
                'status': 1
            }
            send_sms(
                str(UserAuthCode.objects.get(user=user).code),
                '+12065550100',
                [f'+98{user.phone}'],
                fail_silently=False
            )
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

                send_sms(
                    str(UserAuthCode.create_or_get_and_delete(user).code),
                    '+12065550100',
                    [f'+98{request.data["phone"]}'],
                    fail_silently=False
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
                        login(request, user)
                        user_code.delete()
                        token.delete()
                        Token.objects.create(user=user)

                    else:
                        data['status'] = 'invalid code', 20
                else:
                    user_code.delete()
                    new_code = UserAuthCode.objects.create(user=user)
                    data['status'] = 'time is up', 30
                    send_sms(
                        str(new_code.code),
                        '+12065550100',
                        [f'+98{new_code.user.phone}'],
                        fail_silently=False
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
                user_code = UserAuthCode.objects.get(user=user)
                user_code.delete()
                new_code = UserAuthCode.objects.create(user=user)
                data['status'] = 'ok', 20
                send_sms(
                    str(new_code.code),
                    '+12065550100',
                    [f'+98{new_code.user.phone}'],
                    fail_silently=False
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
