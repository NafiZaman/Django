from .models import *
from django.contrib import admin

class PostAdminConfig(admin.ModelAdmin):
    search_fields = ['op',]
    ordering = ("-op",)
    list_display = ("op", "id", "date_added")

    fieldsets = (
        ('Post Information', {'fields': ('op', 'text', 'date_added',)}),
    )

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

class PostLikeAdminConfig(admin.ModelAdmin):
    search_fields = ['user',]
    ordering = ("-user",)
    list_display = ("post",)

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

class PostCommentAdminConfig(admin.ModelAdmin):
    search_fields = ['commenter',]
    ordering = ("-commenter",)
    list_display = ("post",)

    fieldsets = (
        ('Post Comment Information', {'fields': ('commenter', 'post.id', 'text', 'date_added',)}),
    )

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

class PostCommentLikeAdminConfig(admin.ModelAdmin):
    search_fields = ['user',]
    ordering = ("-user",)
    list_display = ("post_comment", "is_liked", )

    fieldsets = (
        ('Post Comment Information', {'fields': ('user', 'post_comment.post.id', 'post_comment_text', 'is_liked',)}),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# class PostCommentSentimentAdminConfig(admin.ModelAdmin):
#     search_fields = ['user',]
#     ordering = ("-user",)
#     list_display = ("post_comment", "is_liked", "is_disliked")

#     fieldsets = (
#         ('Post Comment Information', {'fields': ('user', 'post_comment.post.id', 'post_comment_text', 'is_liked', 'is_disliked',)}),
#     )
    
#     def has_add_permission(self, request):
#         return False
    
#     def has_change_permission(self, request, obj=None):
#         return False

admin.site.register(Post, PostAdminConfig)
admin.site.register(PostLike, PostLikeAdminConfig)
admin.site.register(PostComment, PostCommentAdminConfig)
admin.site.register(PostCommentLike, PostCommentLikeAdminConfig)
# admin.site.register(PostCommentSentiment, PostCommentSentimentAdminConfig)