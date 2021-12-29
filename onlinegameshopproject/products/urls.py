from bookings.views import customer_bookings
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # path('', 'home:home'),
    path('', views.featured_products, name="featured_products"),
    path('view_product/<int:product_id>',
         views.view_product, name='view_product'),
    # path('search/', views.search_product, name="search_product")
]
