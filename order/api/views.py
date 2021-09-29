import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldDoesNotExist
from django.http import FileResponse, JsonResponse
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from rest_framework import mixins, generics, serializers
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from constants.vars import STATES
from customer.api.serializers import CustomerSerializer, StateCitiesSerializer
from customer.models import Customer
from order.api.serializers import CartItemSerializer
from order.models import Cart
from product.models import Product
from product.templatetags.product_extras import get_final_price_for_a_product
from utils.utils_functions import check_for_dict_values, phone_validator, email_validator, get_static, \
    get_states_and_cities

User = get_user_model()


class TestView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = {}
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():

            token = serializer.data['token']
            product, product_property, product_color, number = serializer.data['product'], serializer.data[
                'product_property'], serializer.data['product_color'], serializer.data['number']

            if token:
                customer = Customer.get_by_token(token)
                cart = Cart.objects.get_or_create(customer=customer, status='active')[0]
                cart.add_item(product=product,
                              product_property=product_property,
                              product_color=product_color,
                              number=number)

            product = Product.get_or_none(product)
            if product:
                cart_item_price = product.calc_price_base_of_color_and_factor_property(
                    property_id=product_property,
                    color_id=product_color)

                if not (product_property or product_color):
                    cart_item_price = cart_item_price[0]

                return Response({'price': cart_item_price * int(number),
                                 'price_with_discount': get_final_price_for_a_product(
                                     cart_item_price * number, product.id)})

            return Response({'ok': 1})

        return Response(serializer.data)
