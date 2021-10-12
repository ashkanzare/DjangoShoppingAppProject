from django.urls import path

from order.views import CartView, CreateOrderView, PaymentView

app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('shipping/', CreateOrderView.as_view(), name='order'),
    path('payment/', PaymentView.as_view(), name='payment')
]
