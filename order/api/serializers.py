from rest_framework import serializers
from rest_framework.authtoken.models import Token

from customer.models import Address, Customer
from order.models import CartItem, Order, Cart
import constants.vars as const


class CartItemSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=40, allow_blank=True)

    class Meta:
        model = CartItem
        fields = ['token', 'product', 'product_color', 'product_property', 'number']


class TokenSessionSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100, allow_blank=True)
    session = serializers.CharField(max_length=100, allow_blank=True)


class CreateOrderSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=100, allow_blank=True, required=False)
    cart_id = serializers.IntegerField(required=False)
    address_id = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        fields = ['token', 'address_id', 'cart_id', 'shipping_type']

    def to_internal_value(self, data):
        cart_id = data.get('cart_id')
        address_id = data.get('address_id')
        token_key = data.get('token')

        # Perform the data validation.
        if not token_key:
            raise serializers.ValidationError({
                'token': "Token can't be empty."
            })

        token = Token.objects.filter(key=token_key)

        if not token:
            raise serializers.ValidationError({
                'user': "User does not exist."
            })

        if not (cart_id.isnumeric() and address_id.isnumeric()):
            raise serializers.ValidationError({
                'cart': 'Cart id and address id must be number.'
            })

        user = token[0].user
        cart = Cart.objects.filter(pk=cart_id, status=const.CART_ACTIVE, customer__user=user)

        if not cart:
            raise serializers.ValidationError({
                'cart': 'Cart does not exist.'
            })

        address = Address.objects.filter(pk=address_id, customer__user=user)
        if not address:
            raise serializers.ValidationError({
                'address': 'Address does not match.'
            })

        data_dict = data.dict()
        del data_dict['token']

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return super(CreateOrderSerializer, self).to_internal_value(data=data_dict)

    def save(self, **kwargs):
        order = Order.objects.filter(cart=self.data['cart_id'])
        if not order:
            return super(CreateOrderSerializer, self).save(**kwargs)
        return order[0]
