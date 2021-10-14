from django.urls import path

from order.views import CartView, CreateOrderView, PaymentView, PaymentDetailView, OrderDetailView

app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('shipping/', CreateOrderView.as_view(), name='order'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/<str:payment_method>/<int:order_id>', PaymentDetailView.as_view(), name='payment-info'),
    path('payment/<int:order_id>', OrderDetailView.as_view(), name='order-detail')
]
