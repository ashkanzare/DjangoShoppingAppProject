from django.contrib import admin
from .models import Customer, DiscountCode, Address

# Register your models here.
admin.site.register(Customer)
admin.site.register(Address)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    raw_id_fields = ("customer",)
