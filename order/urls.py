from django.urls import path

from order.views import CartView

app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart')
]
