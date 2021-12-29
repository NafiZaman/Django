from django.urls import path
from . import views

app_name = 'friend'

urlpatterns = [
    path('', views.friends, name="friends"),
    path('sendFriendRequest/', views.send_friend_request, name='send_friend_request'),
    path('acceptFriendRequest/', views.accept_friend_request, name="accept_friend_request"),
    path('unfriend/', views.unfriend, name='unfriend'),
]