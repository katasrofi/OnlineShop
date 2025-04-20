# Orders Urls
from django.urls import path
from . import views

app_name = "orders_shop"

urlpatterns = [
    path("checkout_order/<str:pk>/", views.checkout_order, name="checkout_order"),
    path("payment/<str:payment_id>", views.process_payment_view, name="process_payment"),
]
