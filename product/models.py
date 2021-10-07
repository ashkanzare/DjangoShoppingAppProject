import webcolors
from django.db import models

import constants.vars as const
from utils.utils_functions import image_path_generator
from easy_thumbnails.files import get_thumbnailer

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
    quantity = models.IntegerField(default=0, verbose_name=const.QUANTITY, help_text=const.QUANTITY_HELP_TEXT)
    factor_property = models.ForeignKey(ProductProperty, on_delete=models.CASCADE, verbose_name=const.FACTOR_PROPERTY,
                                        null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"[ {self.id} ] -- [ {self.category.name} ] -- [ {self.name} ]"

    def get_first_image(self):
        """ get first product image for showing in main page """
        image = ProductImage.objects.filter(product__id=self.id).first()
        return image

    def calc_final_price(self):
        """ calculate base price of a product with discount """
        discount = ProductDiscount.get_or_none(self.id)
        if discount:
            if discount.percent_mode:
                return True, discount.product.price * (1 - discount.discount_amount / 100), discount.discount_amount
            return False, self.price - discount.discount_amount
        return None, self.price

    def calc_final_price_with_properties(self, property_id, color_id):
        """ calculate base price of a product with discount """
        discount = ProductDiscount.get_or_none(self.id)
        if discount:
            product_price = discount.product.calc_price_base_of_color_and_factor_property(property_id, color_id)
            product_price = product_price[0] if isinstance(product_price, tuple) else product_price

            if discount.percent_mode:
                return product_price * (1 - discount.discount_amount / 100), discount.discount_amount, product_price
            return product_price - discount.discount_amount, discount.discount_amount, product_price

        product_price = self.calc_price_base_of_color_and_factor_property(property_id, color_id)
        product_price = product_price[0] if isinstance(product_price, tuple) else product_price
        return product_price, 0, product_price

    def calc_final_price_with_default_properties(self):
        """ calculate property base price of a product with discount """
        product_property = self.productfactorproperty_set.filter(quantity__gte=1).first()
        product_color = self.productcolor_set.filter(quantity__gte=1).first()
        price_with_properties = self.price + (product_property.price_impact if product_property else 0)
        total_price = price_with_properties + (product_color.price_impact if product_color else 0)
        discount = ProductDiscount.get_or_none(self.id)
        if discount:
            if discount.percent_mode:
                return True, total_price * (1 - discount.discount_amount / 100), discount.discount_amount, total_price
            return False, total_price - discount.discount_amount, total_price
        return None, total_price

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

    def check_colors(self):
        """ check if product has colors """
        if self.quantity == 0:
            color_quantity = self.productcolor_set.filter(quantity__gte=1)
            return True, color_quantity if color_quantity else 0
        return False, self.quantity

    def check_for_guarantee(self):
        """ check if product has guarantee """
        try:
            return self.propertydescription_set.get(property__name='گارانتی')
        except PropertyDescription.DoesNotExist:
            return None

    def check_quantity(self):
        """ check if product has quantity base of factor property """
        if self.quantity == 0:
            factor_quantity = self.productfactorproperty_set.filter(quantity__gte=1)
            return True, factor_quantity if factor_quantity else 0
        return False, self.quantity

    def check_properties(self):
        """ calculate price base of factor property if it exists """
        factor_quantity = self.productfactorproperty_set.filter(quantity__gte=1)
        if factor_quantity:
            impact_price = factor_quantity.first().price_impact
            return self.price + impact_price, factor_quantity.first()
        return self.price, None

    def get_top_3_properties(self):
        """ get top 3 property for showing in the top div """
        properties = self.propertydescription_set.filter(show_in_top_properties=True)
        properties_length = len(properties)
        if properties_length != 3:
            count = abs(3 - properties_length)
            show_property_bool = False if 3 > properties_length else True
            properties = self.propertydescription_set.filter(show_in_top_properties=show_property_bool)[:count]
            for property_ in properties:
                property_.show_in_top_properties = not show_property_bool
                property_.save()
            return self.propertydescription_set.filter(show_in_top_properties=not show_property_bool)
        return properties

    def get_images_thumbnail(self):
        """ return thumbnail images url of the product """
        options = {'size': (120, 120), 'crop': True}
        return [get_thumbnailer(p.image).get_thumbnail(options).url for p in self.productimage_set.all()]

    def check_all_quantity(self):
        """ check product quantity base of factor property or color """
        if self.quantity == 0:
            factor_quantity = self.productfactorproperty_set.filter(quantity__gte=1)
            color_quantity = self.productcolor_set.filter(quantity__gte=1)
            if factor_quantity:
                return True, factor_quantity
            elif color_quantity:
                return True, color_quantity
        return False, self.quantity

    def calc_price_base_of_color_and_factor_property(self, property_id=None, color_id=None):
        """ calculate price of a product base of a factor property and color property """
        if not (property_id or color_id):
            return self.price, self.calc_final_price()
        else:
            factor_properties = self.productfactorproperty_set.filter(pk=property_id if property_id else None)
            color_property = self.productcolor_set.filter(pk=color_id if color_id else None)
            print('factor', self.productfactorproperty_set.filter(pk=property_id), 'color', color_property)
            price_with_properties = self.price + (factor_properties[0].price_impact if factor_properties else 0)
            total_price = price_with_properties + (color_property[0].price_impact if color_property else 0)
            print('total', total_price)
            return total_price


class ProductFactorProperty(models.Model):
    """
        ProductFactorProperty Model contains:
                product(required),
                property(required),
                value(required),
                price_impact(optional),
                quantity(optional),
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=const.PRODUCT)
    value = models.CharField(max_length=500, verbose_name=const.FACTOR_PROPERTY_VALUES)
    price_impact = models.FloatField(default=0, verbose_name=const.PRICE_IMPACT)
    quantity = models.PositiveIntegerField(default=0, verbose_name=const.QUANTITY)

    def __str__(self):
        return f"[ {self.product.id} ] -- " \
               f"[ {self.product.factor_property.name if self.product.factor_property else '-'} ] " \
               f"-- [ {self.value} ] -- [ {self.quantity} ]"

    @classmethod
    def get_price_base_of_property(cls, property_id):
        try:
            product_property = ProductFactorProperty.objects.get(pk=property_id)
            price = product_property.price_impact + product_property.product.price
            return price
        except ProductFactorProperty.DoesNotExist:
            return None


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=const.COLOR)
    color = models.CharField(max_length=100, choices=const.COLOR_CHOICES)
    price_impact = models.FloatField(default=0, verbose_name=const.PRICE_IMPACT)
    quantity = models.PositiveIntegerField(default=0, verbose_name=const.QUANTITY)

    def __str__(self):
        return f"[ {self.product.id} ] -- [ {self.product.name} ] -- [ {webcolors.hex_to_name(self.color)} ] "

    @classmethod
    def get_price_base_of_color(cls, color_id):
        try:
            product_color = ProductColor.objects.get(pk=color_id)
            price = product_color.price_impact + product_color.product.price
            return price
        except ProductColor.DoesNotExist:
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
    show_in_top_properties = models.BooleanField(default=False)

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

    @classmethod
    def get_or_none(cls, product_id):
        """ get a object of ProductDiscount if it exists else return None """
        product_discount = None
        try:
            product_discount = ProductDiscount.objects.get(product__id=product_id)
        except ProductDiscount.DoesNotExist:
            pass
        finally:
            return product_discount
