from . models import Friend
from django.contrib import admin

class FriendAdminConfig(admin.ModelAdmin):
    search_fields = ['sender',]
    ordering = ("-sender",)
    list_display = ("sender", "receiver", "confirmed",)

    fieldsets = (
        ('Profile Information', {'fields':('sender', 'receiver', 'confirmed', 'date_added',)}),
    )

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Friend, FriendAdminConfig)