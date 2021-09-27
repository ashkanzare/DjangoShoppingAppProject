from django.db.models import Q
from rest_framework import serializers
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.api.serializers import ProductSerializer, CategoryProductSerializer, BaseProductSerializer, \
    BasicCategorySerializer, ProductByIdSerializer, PropertyDescriptionSerializer, ProductImageSerializer, \
    PropertyByIdSerializer, ColorAndPropertyByIdSerializer, CategoryAndProductSerializer
from product.models import Product, Category, PropertyDescription, ProductFactorProperty, ProductColor
from product.templatetags.product_extras import get_final_price_for_a_product


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


class GetProductByCategoryExceptGivenIdView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get all products by category name """
    queryset = {}
    serializer_class = CategoryAndProductSerializer

    def post(self, request, *args, **kwargs):
        category = self.request.data['category']
        product = self.request.data['product']
        queryset = Product.objects.filter(
            (Q(category__id=category) | Q(category__parent__id=category)) if category.isnumeric() else
            (Q(category__name__contains=category) | Q(category__parent__name__contains=category))).exclude(id=product)
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


class GetProductImagesByIdView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get a product's images by it's id """
    queryset = {}
    serializer_class = ProductByIdSerializer

    def post(self, request, *args, **kwargs):
        product_id = self.request.data['product_id']
        queryset = Product.get_or_none(product_id)

        if queryset:
            serialized_queryset = ProductImageSerializer(

                queryset.productimage_set.all(),
                context={'request': request},
                many=True).data

            return Response(serialized_queryset)

        return Response({})


class GetPriceByPropertyView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get the price base of the factor property """
    queryset = {}
    serializer_class = PropertyByIdSerializer

    def post(self, request, *args, **kwargs):
        property_id = self.request.data['property_id']
        price = ProductFactorProperty.get_price_base_of_property(property_id)
        if price:
            return Response({'price': price})
        return Response({})


class GetPriceByColorView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get the price base of the color property """
    queryset = {}
    serializer_class = PropertyByIdSerializer

    def post(self, request, *args, **kwargs):
        property_id = self.request.data['property_id']
        price = ProductColor.get_price_base_of_color(property_id)
        if price:
            return Response({'price': price})
        return Response({})


class GetPriceByColorAndFactorPropertyView(mixins.ListModelMixin, generics.GenericAPIView):
    """ Get the price base of the color property """
    queryset = {}
    serializer_class = ColorAndPropertyByIdSerializer

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        property_id = self.request.data['property_id']
        color_id = self.request.data['color_id']
        product_id = self.request.data['product_id']

        product = Product.get_or_none(product_id)
        if product:
            price = product.calc_price_base_of_color_and_factor_property(property_id, color_id)
            return Response({'price': price,
                             'price_with_discount': get_final_price_for_a_product(price, product.id)})
        return Response({})
