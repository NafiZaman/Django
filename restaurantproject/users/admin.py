from django.contrib import admin
from . models import NewUser, Customer
from django.contrib.auth.admin import UserAdmin

# class UserAdminConfig(UserAdmin):
#     ordering = ('-email',)
#     list_display = ('email', 'is_superuser', 'is_staff', 'is_active', 'last_login')

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Permissions', {
#          'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
#         ('Other Information', {'fields': ('last_login',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_active')
#         }),
#     )

class CustomerAdminConfig(UserAdmin):
    ordering = ('-email',)
    list_display = ('email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        ('User Information', {'fields': ('email', 'password',)}),
        ('Personal Information', {'fields': ('phone_number',)}),

        ('Permissions', {
         'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
        ('Other Information', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)
        }),
    )

# admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Customer, CustomerAdminConfig)

