from rest_framework import viewsets, mixins, generics

from user.api.serializers import UserSerializer, CustomerUserSerializer
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerUserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.filter(is_customer=True)
    serializer_class = CustomerUserSerializer

