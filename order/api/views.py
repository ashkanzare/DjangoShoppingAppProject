from django.contrib.auth import get_user_model

from rest_framework import mixins, generics
from rest_framework.response import Response

from customer.models import Customer
from order.api.serializers import CartItemSerializer
from order.models import Cart
from product.models import Product
from product.templatetags.product_extras import get_final_price_for_a_product

User = get_user_model()


class AddToCartView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = {}
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        response = {'status': 30}
        if serializer.is_valid():

            token = serializer.data['token']
            product, product_property, product_color, number = list(map(lambda x: int(x) if x else None, [
                serializer.data['product'],
                serializer.data['product_property'],
                serializer.data['product_color'],
                serializer.data['number']]))

            cart = None
            if token:

                customer = Customer.get_by_token(token)
                cart = Cart.objects.get_or_create(customer=customer, status='active')[0]
                item_added, status = cart.add_item(product=product,
                                                   product_property=product_property,
                                                   product_color=product_color,
                                                   number=number)

                if item_added:
                    response['status'] = 20

                response['item_add_delete_status'] = status

            product = Product.get_or_none(product)
            if product:

                cart_item_price = product.calc_price_base_of_color_and_factor_property(
                    property_id=product_property,
                    color_id=product_color)

                if not (product_property or product_color):
                    cart_item_price = cart_item_price[0]

                return Response({'price': cart_item_price * int(number),
                                 'price_with_discount': get_final_price_for_a_product(
                                     cart_item_price * number, product.id),
                                 'cart_count': len(cart.cartitem_set.all()) if cart else None,
                                 'status': response['status']})

            return Response(response)

        return Response(response)
