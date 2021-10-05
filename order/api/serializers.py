from rest_framework import serializers
from order.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=40, allow_blank=True)

    class Meta:
        model = CartItem
        fields = ['token', 'product', 'product_color', 'product_property', 'number']


class TokenSessionSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100, allow_blank=True)
    session = serializers.CharField(max_length=100, allow_blank=True)
