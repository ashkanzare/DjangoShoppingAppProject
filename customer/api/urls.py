from django.urls import path, include
from rest_framework import routers

from customer.api.views import (
    CustomerEditDetail
)

app_name = 'customer_api'

urlpatterns = [
    path('', CustomerEditDetail.as_view(), name='customer-edit'),
]
