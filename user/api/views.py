from django.contrib.auth import login
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sms import send_sms

from user.api.serializers import UserSerializer, CustomerUserSerializer, UserAuthCodeSerializer
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
            user = serializer.save()
            user.is_customer = True
            user.is_active = False
            data['response'] = 'user created successfully'
            data['phone'] = user.phone
            data['token'] = Token.objects.get(user=user).key
            data['active'] = user.is_active
            data['status'] = 1
            send_sms(
                str(UserAuthCode.objects.get(user=user).code),
                '+12065550100',
                ['+441134960000'],
                fail_silently=False
            )
        else:
            data['error'] = serializer.errors
            data['status'] = 0
        return Response(data)


@api_view(['POST', ])
def check_user_code(request):
    if request.method == 'POST':
        serializer = UserAuthCodeSerializer(data=request.data)
        data = {}
        print(request.data)
        if serializer.is_valid():
            try:
                user_by_token = Token.objects.get(key=request.data['token']).user
                user_code = UserAuthCode.objects.get(user=user_by_token)
                if user_code.code == request.data['code']:
                    data['status'] = 'ok'
                    data['active'] = user_by_token.is_active = True
                    login(request, user_by_token)
                    user_code.delete()
                else:
                    data['status'] = 'invalid code'
            except (UserAuthCode.DoesNotExist, Token.DoesNotExist):
                data['status'] = 'invalid input'
        else:
            data['error'] = serializer.errors
        return Response(data)
