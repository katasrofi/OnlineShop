# User Urls 
from django.urls import path
from . import views 

urlpatterns = [
    path('product_item', Product.as_view(), name='product_item')    
]
