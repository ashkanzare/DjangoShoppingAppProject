from django.contrib import admin
from .models import Customer, DiscountCode, Address, MeCoinWallet

""" Customer App's Models Register """

admin.site.register(Address)


class MeCoinWalletTabularInline(admin.TabularInline):
    model = MeCoinWallet


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('discount_code',)
    raw_id_fields = ("customer",)  # can search user by phone number and returns their customer_id


@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    inlines = [MeCoinWalletTabularInline, ]
