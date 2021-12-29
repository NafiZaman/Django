from os import name
from django.urls import path
from . import views

app_name = 'uploads'

urlpatterns = [
    path('', views.my_uploads, name='my_uploads'),
    path('removeUpload/', views.remove_upload, name='remove_upload'),
    path('setProfilePic/', views.set_profile_pic, name="set_profile_pic"),
]