from django.urls import path

from product.views import ProductView, CategoryProductsView

app_name = 'product'

urlpatterns = [
    path('product-detail/<int:product_id>', ProductView.as_view(), name='product-detail'),
    path('category/<int:category_id>', CategoryProductsView.as_view(), name='category-detail')
]
