from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.user_profile_home),
    # path('shop/', views.shop, name='shop'),
    path('shop/new_products/', views.new_products, name="new_products"),
    path('shop/my-products/', views.my_products, name='my_products'),
]
