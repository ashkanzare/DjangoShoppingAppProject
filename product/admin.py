from django.contrib import admin
from product.models import Category, PropertyDescription, ProductProperty, Product, ProductImage, ProductDiscount

""" Property App's Models Register """


class PropertyDescriptionTabularInline(admin.TabularInline):
    model = PropertyDescription
    autocomplete_fields = ['property']


class ProductImageTabularInline(admin.TabularInline):
    model = ProductImage
    max_num = 3


class DiscountProductTabularInline(admin.TabularInline):
    model = ProductDiscount
    max_num = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['category__name', 'name']
    autocomplete_fields = ['category']
    inlines = [PropertyDescriptionTabularInline, ProductImageTabularInline, DiscountProductTabularInline]
    list_filter = ['category']


@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    search_fields = ['category__name']


@admin.register(PropertyDescription)
class PropertyDescriptionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['property', 'product']
