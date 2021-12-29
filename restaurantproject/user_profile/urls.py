from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    # path('<int:profile_id>', views.view_profile, name='view_profile'),
    # path('like_post', views.like_post, name='like_post')
]
