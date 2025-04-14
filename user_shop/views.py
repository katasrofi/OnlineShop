"""
user_shop module:

ThiS module handle account management:
*Function :
--------------
 ** RegisterPage()
        Create Account and hash the account password
 ** LoginPage()
        Check the login is valid or Invalid
 ** LogoutPage()
        Logout 

NOTE:
 * RegisterPage can't create super account 

"""
from django.urls import reverse_lazy
from django.shortcuts import (
        render, 
        redirect
)
from django.contrib import (
        auth, 
        messages
)
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.views.generic.edit import FormView 
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import RegisterForm
from .serializers import EmailTokenObtainPairSerializer


# Create your views here.
class RegisterPage(FormView):
    template_name = "user_shop/register_page.html"
    form_class = RegisterForm
    success_url = reverse_lazy("base:home")

    def form_valid(self, form):
        # Save user
        user = form.save(commit=False)
        user.email = user.email.lower()
        user.save()

        # Login after registtration
        auth.login(self.request, user)
        messages.success(self.request, "You have registration successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM INVALID!")  # Debugging
        print(form.errors)  # Cek error form di terminal
        messages.error(self.request, "Registration failed. Please check your input.")
        return super().form_invalid(form)

# Login Page View
class LoginPage(LoginView):
    template_name = "user_shop/login_page.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Get account data
        email = self.request.POST.get("username")
        password = self.request.POST.get("password")

        # Authenticate the account
        user = auth.authenticate(self.request, email=email, password=password)

        # Print Success
        if user is not None:
            auth.login(self.request, user)
            messages.success(self.request, "You have successfully login")
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    # Invalid Form
    def form_invalid(self, form):
        # Debugging
        print("FORM INVALID!")
        print("POST DATA:", self.request.POST)
        print("ERRORS:", form.errors)
        email = self.request.POST.get("email")

        # Check the account exists or not
        if not auth.get_user_model().objects.filter(email=email).exists():
            messages.error(self.request, "Account doesn't exists")
        else:
            messages.error(self.request, "Wrong Password")

        return super().form_invalid(form)

    # Return to home after login
    def get_success_url(self):
        return reverse_lazy("base:home")

# Serializers Login Page 
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class LogoutPage(LogoutView):
    next_page = reverse_lazy("base:home")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "You have successfully Logout")
        return super().dispatch(request, *args, **kwargs)
