from django.contrib import admin
from .models import NewUser, Shop, Customer
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    ordering = ('-email',)
    list_display = ('email', 'is_superuser',
                    'is_staff', 'is_active', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
         'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
        ('Other Information', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active')
        }),
    )


class ShopAdminConfig(UserAdmin):
    ordering = ('-email',)
    list_display = ('email', 'shop_name', 'date_joined', 'is_active')

    fieldsets = (
        ('User Information', {'fields': ('shop_name',
         'email', 'password',)}),
        ('Contact Information', {
         'fields': ('city', 'country', 'zipcode', 'phone',)}),
        ('Permissions', {
            'fields': ('is_active', 'groups')}),
        ('Other Information', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'shop_name', 'password1', 'password2')
        }),
    )

    exclude = ('first_name', 'last_name', 'username')


class CustomerAdminConfig(UserAdmin):
    ordering = ('-email',)
    list_display = ('email', 'username', 'date_joined', 'is_active')

    fieldsets = (
        ('User Information', {'fields': ('username',
         'email', 'password',)}),
        ('Personal Information', {'fields': ('first_name',
                                             'last_name')}),
        ('Contact Information', {
         'fields': ('city', 'country', 'zipcode', 'phone',)}),
        ('Permissions', {
            'fields': ('is_active', 'groups')}),
        ('Other Information', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Shop, ShopAdminConfig)
admin.site.register(Customer, CustomerAdminConfig)
