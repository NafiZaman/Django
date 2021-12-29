from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('get_product/', views.get_product),
    path('view_product/<str:product_id>', views.view_product, name='view_product'),
    path('rate_review/', views.rate_review, name="rate_review"),
    path('search_product/', views.search_product, name='search_product'),
    # path('view_product/<int:product_id>/',
    #      views.ProductDetailsView.as_view(), name='view_product')
]
