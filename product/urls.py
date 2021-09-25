from django.urls import path

from product.views import ProductView

app_name = 'product'

urlpatterns = [
    path('product-detail/<int:product_id>', ProductView.as_view(), name='product-detail')
]
