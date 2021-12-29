from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('settings/', views.user_settings, name='user_settings'),
    path('search/', views.search_people, name='search'),
]