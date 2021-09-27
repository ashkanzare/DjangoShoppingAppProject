from django.urls import path, include
from rest_framework import routers

from product.api.views import (
    get_all_products,
    GetProductByCategoryView,
    GetAllCategoriesView,
    GetProductByIdView,
    GetProductImagesByIdView,
    GetPriceByPropertyView,
    GetPriceByColorView,
    GetPriceByColorAndFactorPropertyView,
    GetProductByCategoryExceptGivenIdView
)

app_name = 'product_api'

urlpatterns = [
    path('', get_all_products, name='products-api'),
    path('product-by-category/', GetProductByCategoryView.as_view(), name='category-products-api'),
    path('category-exclude-product/', GetProductByCategoryExceptGivenIdView.as_view(),
         name='category-exclude-product-api'),
    path('categories/', GetAllCategoriesView.as_view(), name='categories-api'),
    path('product-info/', GetProductByIdView.as_view(), name='product-info-api'),
    path('product-images/', GetProductImagesByIdView.as_view(), name='product-images-api'),
    path('product-price-by-property/', GetPriceByPropertyView.as_view(), name='product-price-by-property-api'),
    path('product-price-by-color/', GetPriceByColorView.as_view(), name='product-price-by-color-api'),
    path('product-price-by-color-and-property/', GetPriceByColorAndFactorPropertyView.as_view(),
         name='product-price-by-color-and-property-api'),
]
