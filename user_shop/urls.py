# User Urls
from django.urls import path
from . import views

app_name = "user_shop"

urlpatterns = [
    path("register/", views.RegisterPage.as_view(), name="register"),
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.LogoutPage.as_view(), name="logout"),
]
