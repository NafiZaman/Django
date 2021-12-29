from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.shops_home),
    path('new_products/', views.new_products, name="new_products"),
    path('my-products/', views.my_products, name='my_products'),
]
