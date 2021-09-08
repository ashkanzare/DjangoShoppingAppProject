from django.contrib import admin
from .models import Customer, DiscountCode, Address

""" Customer App's Models Register """

admin.site.register(Customer)
admin.site.register(Address)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('discount_code', )
    raw_id_fields = ("customer",)  # can search user by phone number and returns their customer_id
