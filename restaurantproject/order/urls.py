from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my_orders/', views.my_orders, name="my_orders"),
]
