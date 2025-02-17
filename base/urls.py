# Base Urls
from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
]
