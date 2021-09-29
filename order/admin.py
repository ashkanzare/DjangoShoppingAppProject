from django.contrib import admin
from order.models import Cart, CartItem, Order

admin.site.register(Order)


class CartItemInline(admin.StackedInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline, ]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ['product_color']