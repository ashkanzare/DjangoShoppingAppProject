from django.urls import path, include
from rest_framework import routers

from product.api.views import (
    get_all_products,
    GetProductByCategoryView,
    GetAllCategoriesView
)

app_name = 'product_api'

urlpatterns = [
    path('', get_all_products, name='products-api'),
    path('product-by-category/', GetProductByCategoryView.as_view(), name='category-products-api'),
    path('categories/', GetAllCategoriesView.as_view(), name='categories-api'),
]
