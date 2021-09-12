from django import forms
from django.contrib import admin

from .models import Category, PropertyDescription, ProductProperty, Product

# Register your models here.


class PropertyDescriptionTabularInline(admin.TabularInline):
    model = PropertyDescription
    autocomplete_fields = ['property']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['category__name', 'name']
    autocomplete_fields = ['category']
    inlines = [PropertyDescriptionTabularInline]


@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    search_fields = ['category__name']


@admin.register(PropertyDescription)
class PropertyDescriptionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['property', 'product']

