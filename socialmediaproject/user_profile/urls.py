from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    path('<str:name>/<int:id>/', views.view_profile, name='view_profile'),
]