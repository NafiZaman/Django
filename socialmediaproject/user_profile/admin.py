from django.contrib import admin
from .models import Profile

class ProfileAdminConfig(admin.ModelAdmin):
    search_fields = ['user',]
    ordering = ("-user",)
    list_display = ('user', 'bio')
    # readonly_fields=('user',)

    fieldsets = (
        ('Profile Information', {'fields':('user' ,'bio', 'education', 'rel_status', 'work', 'location',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('user', 'bio', 'interests', 'education', 'rel_status', 'job_status', 'location',)
        }),
    )

    # def has_add_permission(self, request):
    #     return False
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
admin.site.register(Profile, ProfileAdminConfig)
