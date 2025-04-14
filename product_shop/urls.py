# Product Urls
from django.urls import path
from . import views

app_name = "product_shop"

urlpatterns = [ 
    path("product_detail/<str:pk>", views.product_detail, name="product_detail"), 
    # path("product_detail/<str:pk>/", views.ProductDetail.as_view(), name="product_detail"),
    path("search_product/", views.search_product, name="search_product"),
    path("add_category/", views.add_category, name="add_category"),
    path("add_product/", views.add_product, name="add_product"),
    path("product_detail/<str:pk>/edit/", views.edit_product, name="edit_product"),
]
