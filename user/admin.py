from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from .models import UserAuthCode

""" User App's Models Register """
User = get_user_model()


class ShopUserAdmin(UserAdmin):
    search_fields = ['phone']
    ordering = ['id']
    list_display = ['phone']
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (_("User Details"), {'fields': ('phone', 'password')}),
        (_("Account Details"), {'fields': ('date_joined', 'last_login')}),
        (_("Permission"), {'fields': ('is_active', 'is_staff', 'is_customer', 'is_manager')}),
        (_("Group"), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        ("User Details", {'fields': ('phone', 'password1', 'password2')}),
        ("Permission", {'fields': ('is_active', 'is_staff', 'is_manager', 'is_customer')}),

    )


@admin.register(UserAuthCode)
class UserAuthCodeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']


admin.site.register(User, ShopUserAdmin)
