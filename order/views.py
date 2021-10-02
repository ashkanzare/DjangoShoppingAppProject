from django.utils import translation
from django.shortcuts import render
from django.views import generic

from customer.models import Customer
from order.models import Cart
from product.models import Category


class CartView(generic.ListView):
    template_name = 'order/cart.html'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        translation.activate(customer.language)
        user = self.request.user
        cart = Cart.get_or_none(user)

        return cart.cartitem_set.all()
