# Django Library 
from django.db import models

# Create your models here.

class CartShop(models.Model):
    # Relation
    user_id = models.ForeignKey('user_shop.CustomUser',
                                related_name='carts',
                                on_delete=models.CASCADE)
    product_id = models.ForeignKey('product_shop.Product',
                                   related_name='cart_items',
                                   on_delete=models.CASCADE) 

    # Total of product in cart 
    quantity = models.PositiveIntegerField(default=1)

    # Calculate the total price 
    @property 
    def total_price(self):
        return self.product_id.price * self.quantity 
