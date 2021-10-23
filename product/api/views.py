from django.db.models import Q
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import pagination

from product.api.serializers import (ProductSerializer,
                                     CategoryProductSerializer,
                                     BaseProductSerializer,
                                     BasicCategorySerializer,
                                     ProductByIdSerializer,
                                     PropertyDescriptionSerializer,
                                     ProductImageSerializer,
                                     PropertyByIdSerializer,
                                     ColorAndPropertyByIdSerializer,
                                     CategoryAndProductSerializer,
                                     SearchByString,
                                     BaseAPIProductSerializer
                                     )
from product.models import Product, Category, ProductFactorProperty, ProductColor
from product.templatetags.product_extras import get_final_price_for_a_product, price_format


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
        property_id = self.request.data['property_id']
        color_id = self.request.data['color_id']
        product_id = self.request.data['product_id']
        product = Product.get_or_none(product_id)
        if product:
            price = product.calc_price_base_of_color_and_factor_property(property_id, color_id)
            price_with_discount = get_final_price_for_a_product(price, product.id)
            return Response({'price': price_format(price),
                             'price_with_discount': price_format(price_with_discount),
                             'price_with_discount_en': price_with_discount})
        return Response({})


@api_view(['GET', ])
def get_all_category(request):
    """ Get all categories """
    queryset = Category.objects.all()
    final_list = []
    serializer = BasicCategorySerializer
    for category in queryset:
        children = [serializer(child).data for child in Category.objects.filter(parent=category)]
        category_list = {'name': category.name, 'children': children, 'id': category.id,
                         'parent': category.parent.name if category.parent else None}
        final_list.append(category_list)

    return Response(final_list)


class SearchProductView(mixins.ListModelMixin, generics.GenericAPIView):
    """ search in products """
    queryset = {}
    serializer_class = SearchByString

    def post(self, request, *args, **kwargs):
        string = self.request.data['string']
        products = Product.objects.filter(Q(name__icontains=string) | Q(category__name__icontains=string))
        products_with_image = [{
            'id': product.id,
            'name': product.name,
            'image': product.get_first_image().image.url,
            'category': product.category.name
        } for product in products]
        return Response(products_with_image)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 1000

    def change_page_size(self, num):
        self.page_size = num


class GetProductsByCategoryView(generics.ListAPIView):
    """ get products by category id """
    serializer_class = BaseAPIProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        new_pagination = self.request.query_params.get('new_pagination', None)
        if new_pagination and new_pagination.isnumeric():
            self.pagination_class.page_size = int(new_pagination)
        else:
            self.pagination_class.page_size = 1
        return Product.objects.filter(category_id=self.request.query_params.get('category_id', None))


class GetProductByCategoryExceptGivenIdWithPaginationView(generics.ListAPIView):
    """ Get all products by category name """
    pagination_class = StandardResultsSetPagination
    serializer_class = BaseAPIProductSerializer

    def get_queryset(self):
        product = self.request.query_params.get('product_id', 0)
        return Product.objects.filter(category_id=self.request.query_params.get('category_id', None)).exclude(
            id=product)
