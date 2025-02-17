from .models import CustomUser
from django import forms 
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser 
        fields = ['name', 'email', 'phone_number', 'role', 'password1', 'password2']
