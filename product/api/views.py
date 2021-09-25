from django.db.models import Q
from rest_framework import serializers
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.api.serializers import ProductSerializer, CategoryProductSerializer, BaseProductSerializer, \
    BasicCategorySerializer, ProductByIdSerializer, PropertyDescriptionSerializer, ProductImageSerializer
from product.models import Product, Category


@api_view(['GET', ])
def get_all_products(request):
    """ Get all products """
    all_categories = Category.objects.all()
    products = [{category.name: BaseProductSerializer(Product.objects.filter(category__name=category.name),
                                                      context={'request': request}, many=True).data} for
                category in all_categories]
    return Response(products)


class GetAllCategoriesView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get all categories """
    queryset = Category.objects.all()
    serializer_class = BasicCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetProductByCategoryView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get all products by category name """
    queryset = {}
    serializer_class = CategoryProductSerializer

    def post(self, request, *args, **kwargs):
        category = self.request.data['category']
        queryset = Product.objects.filter(
            (Q(category__id=category) | Q(category__parent__id=category)) if category.isnumeric() else
            (Q(category__name__contains=category) | Q(category__parent__name__contains=category)))
        serialized_queryset = ProductSerializer(queryset, context={'request': request}, many=True).data
        return Response(serialized_queryset)


class GetProductByIdView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get a product info by it's id """
    queryset = {}
    serializer_class = ProductByIdSerializer

    def post(self, request, *args, **kwargs):

        product_id = self.request.data['product_id']
        queryset = Product.get_or_none(product_id)

        if queryset:
            serialized_queryset = PropertyDescriptionSerializer(
                queryset.get_properties(),
                context={'request': request},
                many=True).data

            return Response([
                ProductSerializer(queryset, context={'request': request}).data,
                serialized_queryset,
                ProductImageSerializer(queryset.productimage_set.all(), context={'request': request}, many=True).data])

        return Response({})