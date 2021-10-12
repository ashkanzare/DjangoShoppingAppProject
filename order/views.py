from django.utils import translation
from django.shortcuts import render
from django.views import generic

from customer.models import Customer
from order.models import Cart, Order

import constants.vars as const


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


class CreateOrderView(generic.ListView):
    template_name = 'order/create_order.html'
    context_object_name = 'order_info'

    def get_queryset(self):
        cart = Cart.get_or_none(self.request.user)
        customer = Customer.get_by_token(self.request.user.get_token())
        queryset = {'cart': cart,
                    'customer': customer,
                    'MESHOP_SHIPPING': const.MESHOP_SHIPPING,
                    'NORMAL_SHIPPING': const.NORMAL_SHIPPING,
                    'FREE_SHIPPING_MIN_PRICE': const.FREE_SHIPPING_MIN_PRICE
                    }
        return queryset


class PaymentView(generic.ListView):
    template_name = 'order/payment.html'
    context_object_name = 'order_info'

    def get_queryset(self):
        order = Order.get_by_user(self.request.user)
        queryset = {'order': order,
                    'MESHOP_SHIPPING': const.MESHOP_SHIPPING,
                    'NORMAL_SHIPPING': const.NORMAL_SHIPPING,
                    'FREE_SHIPPING_MIN_PRICE': const.FREE_SHIPPING_MIN_PRICE
                    }
        return queryset
