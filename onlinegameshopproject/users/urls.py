from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home_page),
    path('register/<str:user_type>/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    # path('shop_profile/', views.shop_profile, name='shop_profile'),
    # path('shop_profile/add_product', views.add_product, name='add_product')
]
