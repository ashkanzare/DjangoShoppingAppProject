from django.urls import path
from order.api.views import (
    AddToCartView,
    AddToSessionBasedCartView,
    SyncCartsView,
    CreateOrderView

)

app_name = 'order_api'

urlpatterns = [
    path('', AddToCartView.as_view(), name='add-to-cart'),
    path('add-to-session-cart', AddToSessionBasedCartView.as_view(), name='add-to-session-cart'),
    path('sync-carts', SyncCartsView.as_view(), name='sync-carts'),
    path('create-order', CreateOrderView.as_view(), name='create-order'),

]
