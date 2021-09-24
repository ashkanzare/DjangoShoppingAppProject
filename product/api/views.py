from django.db.models import Q
from rest_framework import serializers
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.api.serializers import ProductSerializer, CategoryProductSerializer, BaseProductSerializer
from product.models import Product, Category


@api_view(['GET', ])
def get_all_products(request):
    """ Get all products """
    all_categories = Category.objects.all()
    products = [{category.name: BaseProductSerializer(Product.objects.filter(category__name=category.name),
                                                      context={'request': request}, many=True).data} for
                category in all_categories]
    return Response(products)


class GetProductByCategoryView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get all products by category name """
    queryset = {}
    serializer_class = CategoryProductSerializer

    def post(self, request, *args, **kwargs):
        queryset = Product.objects.filter(
            Q(category__id=self.request.data['category']) | Q(category__parent__id=self.request.data['category']) | Q(
                category__name__contains=self.request.data['category']) | Q(
                category__parent__name__contains=self.request.data['category']))
        serialized_queryset = ProductSerializer(queryset, context={'request': request}, many=True).data
        return Response(serialized_queryset)
