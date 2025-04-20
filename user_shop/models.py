# Django Library
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,
                    email,
                    password=None,
                    **extra_fields):
        if not email:
            raise ValueError("Email need to fill")

        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         password=None,
                         **extra_fields):
        # Set superuser authority
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Validation the superuser authority
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email,
                                password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Users information
    name = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    # Role Choice
    role_choice = [
        ("ADMIN", "ADMIN"),
        ("CUSTOMER", "CUSTOMER"),
        ("SELLER", "SELLER"),
    ]
    role = models.CharField(max_length=20, choices=role_choice, default="CUSTOMER")

    # Registration
    created_at = models.DateTimeField(auto_now_add=True)

    # Status and permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email


class Notification(models.Model):
    # Relation
    user_id = models.ForeignKey(
        CustomUser, related_name="user_notif", on_delete=models.CASCADE
    )

    # Notification information
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
