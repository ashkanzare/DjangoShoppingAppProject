from django.utils import translation
from django.shortcuts import render
from django.views import generic

from customer.models import Customer
from order.models import Cart
from product.models import Category


class CartView(generic.ListView):
    template_name = 'order/cart.html'

    def get_queryset(self):

        user = self.request.user

        if not user.is_anonymous:
            customer = Customer.objects.get(user=user)
            translation.activate(customer.language)
            user = self.request.user
            print(Cart.get_or_none(user))
            return Cart.get_or_none(user)

        else:
            session = self.request.session.session_key
            print(session)
            if session:
                return Cart.get_by_session_or_none(session)
            return None
