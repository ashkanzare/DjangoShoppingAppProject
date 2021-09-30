from django.urls import path, include
from rest_framework import routers

from order.api.views import (
    AddToCartView
)

app_name = 'order_api'

urlpatterns = [
    path('', AddToCartView.as_view(), name='add-to-cart'),

]
