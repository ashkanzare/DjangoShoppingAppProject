from django.http import HttpResponseNotFound
from django.urls import reverse
from django.utils import translation
from django.shortcuts import render, redirect
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
            return Cart.get_or_none(user)

        else:
            session = self.request.session.session_key
            if session:
                return Cart.get_by_session_or_none(session)
            return None


class CreateOrderView(generic.ListView):
    template_name = 'order/create_order.html'
    context_object_name = 'order_info'

    def get_queryset(self):
        cart = Cart.get_or_none(self.request.user)
        customer = Customer.get_by_token(self.request.user.get_token())
        queryset = {}
        if cart:
            queryset = {'cart': cart,
                        'customer': customer,
                        'MESHOP_SHIPPING': const.MESHOP_SHIPPING,
                        'NORMAL_SHIPPING': const.NORMAL_SHIPPING,
                        'FREE_SHIPPING_MIN_PRICE': const.FREE_SHIPPING_MIN_PRICE
                        }
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            return render(request, self.template_name, context={self.context_object_name: queryset})
        return redirect(reverse('order:cart'))


class PaymentView(generic.ListView):
    template_name = 'order/payment.html'
    context_object_name = 'order_info'

    def get_queryset(self):
        order = Order.objects.filter(cart__customer__user=self.request.user, status=const.INITIAL)
        queryset = {}
        if order:
            queryset = {'order': order[0],
                        'MESHOP_SHIPPING': const.MESHOP_SHIPPING,
                        'NORMAL_SHIPPING': const.NORMAL_SHIPPING,
                        'FREE_SHIPPING_MIN_PRICE': const.FREE_SHIPPING_MIN_PRICE
                        }
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            return render(request, self.template_name, context={self.context_object_name: queryset})
        return redirect(reverse('order:cart'))


class PaymentDetailView(generic.ListView):
    template_name = 'order/payment-status.html'
    context_object_name = 'order_info'

    def get_queryset(self):
        order_id = self.kwargs.get('order_id', None)
        payment_method = self.kwargs.get('payment_method', None)
        get_payment_choice = const.ORDER_PAYMENT_REVERSE.get(payment_method, None)
        queryset = {}
        price_per_mecoin = None

        if get_payment_choice:
            if order_id:
                order = Order.get_or_none(order_id=order_id)
                if order and order.status == const.INITIAL:
                    if get_payment_choice == const.MECOIN:
                        price_per_mecoin = order.cart.customer.use_mecoin(order.total_price)

                    queryset = {'order': order,
                                'payment_method': [const.ORDER_PAYMENT_PERSIAN_REVERSE[get_payment_choice],
                                                   get_payment_choice, price_per_mecoin]
                                }
                    order.status = const.PROCESSING
                    order.payment_method = get_payment_choice
                    order.save()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            return render(request, self.template_name, context={self.context_object_name: queryset})
        return HttpResponseNotFound("Page not found")


class OrderDetailView(generic.ListView):
    template_name = 'order/order-detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        order_id = self.kwargs.get('order_id', None)
        order = Order.get_or_none(order_id)
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_object'] = self.get_queryset().cart.customer
        return context
