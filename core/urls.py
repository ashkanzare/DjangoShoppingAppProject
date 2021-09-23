from django.urls import path, include

urlpatterns = [
    path('users/', include('user.api.urls')),
    path('customers/', include('customer.api.urls'))
]
