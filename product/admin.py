from django.contrib import admin
from .models import Category, PropertyDescription, ProductProperty, Product, ProductImage

""" Property App's Models Register """


class PropertyDescriptionTabularInline(admin.TabularInline):
    model = PropertyDescription
    autocomplete_fields = ['property']


class ProductImageTabularInline(admin.TabularInline):
    model = ProductImage
    max_num = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['category__name', 'name']
    autocomplete_fields = ['category']
    inlines = [PropertyDescriptionTabularInline, ProductImageTabularInline]
    list_filter = ['category']


@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    search_fields = ['category__name']


@admin.register(PropertyDescription)
class PropertyDescriptionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['property', 'product']
