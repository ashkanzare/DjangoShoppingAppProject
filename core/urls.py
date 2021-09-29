from django.urls import path, include

urlpatterns = [
    path('users/', include('user.api.urls')),
    path('customers/', include('customer.api.urls')),
    path('products/', include('product.api.urls')),
    path('orders/', include('order.api.urls'))
]
