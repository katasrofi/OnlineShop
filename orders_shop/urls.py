# Orders Urls
from django.urls import path
from . import views

app_name = "orders_shop"

urlpatterns = [
    path("checkout_order/<str:pk>/", views.checkout_order, name="checkout_order"),
]
