from django.core.exceptions import FieldDoesNotExist
from rest_framework import mixins, generics, serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from customer.api.serializers import CustomerSerializer
from customer.models import Customer
from utils.utils_functions import check_for_dict_values, phone_validator, email_validator


# class CustomerEditDetail(mixins.RetrieveModelMixin,
#                          mixins.UpdateModelMixin,
#                          generics.GenericAPIView):
#     queryset = {}
#     serializer_class = serializers.Serializer
#
#     def put(self, request, *args, **kwargs):
#         data = self.request.data
#         if check_for_dict_values(data):
#             try:
#                 token = Token.objects.get(key=data['token'])
#                 user = token.user
#
#                 del data['token']
#                 response = validate_customer_profile_data(data, user, Customer)
#
#                 return Response(response)
#
#             except Token.DoesNotExist:
#                 return Response({
#                     'error': 'wrong token',
#                     'code': 50
#                 })
#         else:
#             return Response({
#                 'error': 'fields must be non-empty',
#                 'code': '30'
#             })

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

        data = {key: data[key] if
                (key in customer[0].__dict__ and (
                        customer[0].__dict__[key] != data[key] or customer[0].__dict__[key] == '')) or (
                        key in token.user.__dict__ and (
                        token.user.__dict__[key] != data[key] or token.user.__dict__[key] == '')) or (
                        key in ['token', 'csrfmiddlewaretoken']) else '' for key in data}

        serializer = self.get_serializer(data=data)
        print(data)
        if serializer.is_valid():
            data.pop('token', None)
            data.pop('csrfmiddlewaretoken', None)
            cleaned_data_customer = {key: data[key] for key in data if data[key] and key not in ['phone', 'email']}
            cleaned_data_user = {key: data[key] for key in data if data[key] and key in ['phone', 'email']}

            token.user.update_by_kwargs(**cleaned_data_user)
            customer.update(**cleaned_data_customer)
            return Response({'status': 20})
        print(serializer.errors)
        return Response(
            {'status': 40,
             'errors': serializer.errors}
        )
