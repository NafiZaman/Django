from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.make_post, name='make_post'),
    path('likePost/', views.like_post, name='like_post'),
    path('addPostComment/', views.add_post_comment, name="add_post_comment"),
    path('likePostComment/', views.like_post_comment, name='like_post_comment'),
    path('updatePost/', views.update_post, name='update_post'),
    path('deletePost/', views.delete_post, name='delete_post'),
    # path('deleteComment/', views.delete_comment, name='delete_comment'),
    # path('add_post_comment_sentiment/', views.add_post_comment_sentiment, name='add_post_comment_sentiment'),
    # path('acceptFriendRequest/', views.accept_friend_request, name="accept_friend_request"),
]