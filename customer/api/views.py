from django.http import JsonResponse
from rest_framework import mixins, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from constants.vars import STATES

from customer.api.serializers import (
    CustomerSerializer,
    StateCitiesSerializer,
    StateCitiesTranslateSerializer,
    UpdateAddressSerializer,
    CreateAddressSerializer
)

from customer.models import Customer
from utils.utils_functions import get_states_and_cities, convert_place_name_to_persian


class CustomerEditDetail(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         generics.GenericAPIView):
    queryset = {}
    serializer_class = CustomerSerializer

    def put(self, request, *args, **kwargs):
        data = dict(self.request.data)
        data = {key: data[key][0] for key in data}

        token = Token.objects.get(key=data['token'])

        customer = Customer.objects.filter(user=token.user)

        data = {key: data[key] if (key in customer[0].__dict__ and (
                customer[0].__dict__[key] != data[key] or customer[0].__dict__[key] == '')) or (
                                          key in token.user.__dict__ and (token.user.__dict__[key] != data[key] or
                                                                          token.user.__dict__[key] == '')) or (
                                          key in ['token', 'csrfmiddlewaretoken']) else '' for key in data}

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            data.pop('token', None)
            data.pop('csrfmiddlewaretoken', None)
            cleaned_data_customer = {key: data[key] for key in data if data[key] and key not in ['phone', 'email']}
            cleaned_data_user = {key: data[key] for key in data if data[key] and key in ['phone', 'email']}

            token.user.update_by_kwargs(**cleaned_data_user)
            customer.update(**cleaned_data_customer)
            return Response({'status': 20})
        return Response(
            {'status': 40,
             'errors': serializer.errors}
        )


class SetCustomerAddress(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = {}
    serializer_class = CreateAddressSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():

            token = serializer.validated_data['token']
            customer = Customer.get_by_token(token)
            if customer:
                serializer.validated_data['customer'] = customer
                del serializer.validated_data['token']

                address = serializer.save()
                return Response({'status': f'address created {address.id}'}, status=status.HTTP_201_CREATED)

            return Response({'status': 'customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCustomerAddress(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = {}
    serializer_class = UpdateAddressSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():

            token = serializer.validated_data['token']
            customer = Customer.get_by_token(token)
            address_id = serializer.validated_data['id']

            if customer:
                serializer.validated_data['customer'] = customer
                customer_address = customer.address_set.filter(pk=address_id)

                if customer_address:
                    del serializer.validated_data['token']
                    del serializer.validated_data['id']

                    customer_address.update(**serializer.validated_data)
                    return Response({'status': 'address updated'}, status=status.HTTP_201_CREATED)

                return Response({'status': 'address does not exist'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'status': 'customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class IranStateCities(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = {}
    serializer_class = StateCitiesSerializer

    def get(self, request, *args, **kwargs):
        return JsonResponse(STATES, safe=False, json_dumps_params={'indent': 2, 'ensure_ascii': False})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            return Response(get_states_and_cities(self.request.data['name']))
        return Response({'cities': 'not found'})


class IranStateCitiesTranslate(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = {}
    serializer_class = StateCitiesTranslateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():
            return Response({
                'name': convert_place_name_to_persian(self.request.data['name'],
                                                      is_city=self.request.data.get('is_city', False)),
                'is_city': self.request.data.get('is_city', False)})
        return Response({'error': 'not found'})
