from django.db import models

import constants.vars as const
from utils.utils_functions import image_path_generator

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
    price = models.FloatField(default=0, verbose_name=const.PRICE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"[ {self.category.name} ] -- [ {self.name} ]"

    def get_first_image(self):
        """ get first product image for showing in main page """
        image = ProductImage.objects.filter(product__id=self.id).first()
        return image

    def calc_final_price(self):
        """ calculate final price of a product with discount """
        discount = ProductDiscount.objects.get(product__id=self.id)
        if discount.percent_mode:
            return True, discount.product.price * (1 - discount.discount_amount / 100), discount.discount_amount
        return False, self.price - discount.discount_amount

    @classmethod
    def get_or_none(cls, product_id):
        """ get a object of product if it exists else return None """
        product = None
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            pass
        finally:
            return product

    def get_properties(self):
        """ get all properties of a product """
        properties = PropertyDescription.objects.filter(product__id=self.id)
        return properties

    def get_all_info(self):
        """ get all info of a product """
        data = {
            'product': self,
            'properties': self.get_properties(),
            'images': self.productimage_set.all()
        }

        return data

    def check_for_guarantee(self):
        try:
            return self.propertydescription_set.get(property__name='گارانتی')
        except PropertyDescription.DoesNotExist:
            return None


class ProductImage(models.Model):
    """
         ProductImage Model contains:
                product(required),
                image(required),

    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=const.PRODUCT)
    image = models.ImageField(upload_to=image_path_generator)

    def __str__(self):
        return f"[ {self.product.name} ]"


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


class ProductDiscount(models.Model):
    """
        ProductDiscount Model contains:
                product(required),
                discount(required),
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount_amount = models.FloatField()
    percent_mode = models.BooleanField(default=True)
    date = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f"[ {self.product.name} ] -- [ {self.discount_amount}{'%' if self.percent_mode else ' T'} ]"
