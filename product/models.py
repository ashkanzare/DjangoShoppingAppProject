from django.db import models

import constants.vars as const

""" Product App's Models """


class Category(models.Model):
    """
         Category Model contains:
                name(required),
                parent(optional),
    """
    name = models.CharField(max_length=250, unique=True, verbose_name=const.NAME)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name=const.PARENT)

    def __str__(self):
        return f"[ Parent: {self.parent.name if self.parent else 0} ] -- [ Child: {self.name} ]"

    class Meta:
        ordering = ('parent__name',)


class ProductProperty(models.Model):
    """
         ProductProperty Model contains:
                name(required),
                parent(required),
    """
    name = models.CharField(max_length=250, unique=True, verbose_name=const.NAME)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=const.CATEGORY)

    def __str__(self):
        return f"[ {self.category.name} ] -- [ {self.name} ]"


class Product(models.Model):
    """
         Product Model contains:
                name(required),
                parent(required),
    """
    name = models.CharField(max_length=1000, verbose_name=const.NAME)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=const.CATEGORY)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"[ {self.category.name} ] -- [ {self.name} ]"


class PropertyDescription(models.Model):
    """
         PropertyDescription Model contains:
                product(required),
                property(required),
                description(required),
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=const.PRODUCT)
    property = models.ForeignKey(ProductProperty, on_delete=models.RESTRICT, verbose_name=const.PROPERTY)
    description = models.CharField(max_length=1000, verbose_name=const.DESCRIPTION)

    def __str__(self):
        return f"[ {self.product.id} ] -- [ {self.property.name} ] -- " \
               f"[ {self.description[:30] + '...' if len(self.description) >= 30 else self.description} ]"
