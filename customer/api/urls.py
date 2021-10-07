from django.urls import path, include
from rest_framework import routers

from customer.api.views import (
    CustomerEditDetail, IranStateCities, IranStateCitiesTranslate
)

app_name = 'customer_api'

urlpatterns = [
    path('', CustomerEditDetail.as_view(), name='customer-edit'),
    path('cities/', IranStateCities.as_view(), name='iran-cities'),
    path('cities-translate/', IranStateCitiesTranslate.as_view(), name='iran-cities-translate'),
]
