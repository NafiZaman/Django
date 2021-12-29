from . models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    search_fields = ['email',]
    ordering = ("-email",)
    list_display = ('email', 'is_superuser', 'is_staff', 'is_active', 'date_joined')

    fieldsets = (
        ('User Information', {'fields': ('email', 'password',)}),
        ('Personal Information', {'fields': ('first_name','last_name', 'dob', 'gender',)}),

        ('Permissions', {
         'fields': ('is_superuser', 'is_staff', 'is_active', 'groups')}),
        ('Other Information', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'dob', 'gender', 'password1', 'password2',)
        }),
    )


class UserSettingAdminConfig(admin.ModelAdmin):
    search_fields = ['user',]
    ordering = ("-user",)
    list_display = ("user", "post_visibility", "profile_visibility", "upload_visibility",)

    fieldsets = (
        ('Profile Information', {'fields':('user', 'post_visibility', 'profile_visibility', 'upload_visibility',)}),
    )

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(NewUser, UserAdminConfig)
admin.site.register(UserSetting, UserSettingAdminConfig)