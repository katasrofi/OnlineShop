# Product Urls
from django.urls import path
from . import views

app_name = "product_shop"

urlpatterns = [ 
    path('product_detail/<str:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('search_product/', views.search_product, name='search_product'),
    path('add_product/', views.add_product, name='add_product')
]
