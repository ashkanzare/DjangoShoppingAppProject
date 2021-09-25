from rest_framework import serializers
from product.models import Product, ProductProperty, PropertyDescription, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    # todo: nested parent
    class Meta:
        model = Category
        fields = ['name']


class BasicCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductByIdSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', min_value=1)

    class Meta:
        model = Product
        fields = ['product_id']


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(default=None, source='product.name', read_only=True)
    price = serializers.FloatField(default=None, source='product.price', read_only=True)
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = '__all__'


class ProductPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProperty
        fields = ['name']


class PropertyDescriptionSerializer(serializers.ModelSerializer):
    property = ProductPropertySerializer()

    class Meta:
        model = PropertyDescription
        fields = ['property', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']
