from django.db import models

# Create your models here.

class CartShop(models.Model):
    product = models.CharField(max_length=200) 
