from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from .models import UserAuthCode


class UserAccountAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['phone']
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (_("User Details"), {'fields': ('phone', 'password')}),
        (_("Account Details"), {'fields': ('date_joined', 'last_login')}),
        (_("Permission"), {'fields': ('is_active', 'is_staff')}),
        (_("Group"), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        ("User Details", {'fields': ('phone', 'password1', 'password2')}),
        ("Permission", {'fields': ('is_active', 'is_staff')}),

    )


admin.site.register(get_user_model(), UserAccountAdmin)
admin.site.register(UserAuthCode)
