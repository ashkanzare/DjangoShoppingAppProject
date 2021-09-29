from django.urls import path, include
from rest_framework import routers

from order.api.views import (
    TestView
)

app_name = 'order_api'

urlpatterns = [
    path('', TestView.as_view(), name='order'),

]
