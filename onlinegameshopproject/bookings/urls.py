from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('<int:stock_id>/', views.new_booking, name="new_booking"),
    path('customer_bookings/', views.customer_bookings, name="customer_bookings"),
    path('shop_bookings/', views.shop_bookings, name="shop_bookings"),
]
