from rest_framework import serializers
from product.models import Product, ProductProperty, PropertyDescription, Category


class CategorySerializer(serializers.ModelSerializer):
    # todo: nested parent
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


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
        fields = '__all__'


class PropertyDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDescription
        fields = '__all__'
