from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username',
                    'user_type', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'user_type', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_active',
         'is_staff', 'user_permissions', 'groups')}),
        ('Important Dates', {'fields': ('date_joined',)}),
        ('User Type', {'fields': ('user_type',)}),
    )
    ordering = ('date_joined',)
    search_fields = ('email', 'first_name', 'last_name', 'username')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'password1', 'password2', 'user_type', 'is_active', 'is_staff')
        }),
    )


admin.site.register(User, UserAdmin)
