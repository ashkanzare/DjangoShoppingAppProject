from django.urls import path

from customer.api.views import (
    CustomerEditDetail,
    IranStateCities,
    IranStateCitiesTranslate,
    SetCustomerAddress,
    UpdateCustomerAddress,
    MeCoinConverter,
    CustomerDiscountCheck,
    DeleteCustomerAddress
)

app_name = 'customer_api'

urlpatterns = [
    path('', CustomerEditDetail.as_view(), name='customer-edit'),
    path('customer-address', SetCustomerAddress.as_view(), name='customer-address'),
    path('update-customer-address', UpdateCustomerAddress.as_view(), name='update-customer-address'),
    path('delete-customer-address', DeleteCustomerAddress.as_view(), name='delete-customer-address'),
    path('cities/', IranStateCities.as_view(), name='iran-cities'),
    path('cities-translate/', IranStateCitiesTranslate.as_view(), name='iran-cities-translate'),
    path('mecoin-converter/', MeCoinConverter.as_view(), name='mecoin'),
    path('check-discount-code/', CustomerDiscountCheck.as_view(), name='check-discount-code'),
]
