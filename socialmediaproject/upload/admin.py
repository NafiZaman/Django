from django.contrib import admin

from .models import UserUpload

class UserUploadAdminConfig(admin.ModelAdmin):
    search_fields = ['upload_type',]
    ordering = ("-date_added",)
    list_display = ("user", "upload_type", "date_added",)

    fieldsets = (
        ('Upload Information', {'fields': ('image', 'upload_type', 'date_added',)}),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(UserUpload, UserUploadAdminConfig)

