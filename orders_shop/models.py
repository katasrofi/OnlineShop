# Django library
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now 
from payments.models import BasePayment

# Create your models here.
class OrderItem(models.Model):
    # Relation 
    user_id = models.ForeignKey('user_shop.CustomUser',
                                related_name='order_users',
                                on_delete=models.CASCADE)

    # Order status 
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    order_status = models.CharField(max_length=30,
                                    choices=STATUS_CHOICES,
                                    default='pending')
    
    # Order detail 
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    # payment_methode = models.CharField(max_length=255)

    @property
    def total_price(self):
        return self.order_detail.aggregate(total=Sum("total_price"))["total"] or 0

class OrderDetail(models.Model):
    # Relation
    order_id = models.ForeignKey(OrderItem, 
                                 related_name='order_detail',
                                 on_delete=models.CASCADE)
    product_id = models.ForeignKey('product_shop.Product',
                                   related_name='order_product',
                                   on_delete=models.CASCADE)

    # Order detail 
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)

    # Calculate the total price 
    def save(self, *args, **kwargs):
        self.total_price = self.product_id.price * self.quantity
        super().save(*args, **kwargs)

class Shipment(models.Model):
    # Relation 
    order_id = models.ForeignKey(OrderItem,
                                 related_name='ship_id',
                                 on_delete=models.CASCADE)

    # Shipment information
    curir = models.CharField(max_length=255)
    resi_number = models.IntegerField()
    
    # Status Choice 
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    shipment_status = models.CharField(max_length=30,
                                       choices=STATUS_CHOICES,
                                       default='pending')
    estimation_time = models.DateTimeField()
    shipment_price = models.DecimalField(max_digits=10,
                                         decimal_places=2)
    
# class Payment(models.Model):
#     # Relation 
#     order = models.ForeignKey(OrderItem,
#                                  related_name='payment',
#                                  on_delete=models.CASCADE)
#
#     # Payment detail 
#     PAYMENT_METHOD_CHOICES = [
#         ('bank_transfer', 'Bank Transfer'),
#         ('debit_card', 'Debit Card'),
#         ('credit_card', 'Credit Card'),
#         ('paypal', 'PayPal'),
#         ('gopay', 'GoPay'),
#         ('ovo', 'OVO'),
#     ]
#     payment_methode = models.CharField(max_length=20,
#                                        choices=PAYMENT_METHOD_CHOICES)
#
#     # Status choices 
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#     ]
#     payment_status = models.CharField(max_length=30,
#                                       choices=STATUS_CHOICES,
#                                       default='pending')
#     payment_date = models.DateTimeField(auto_now_add=True)
#     payment_reference = models.CharField(max_length=50,
#                                          unique=True)
#
#     def __str__(self):
        # return f"{self.order_id} - {self.payment_reference}"

class Payment(BasePayment):
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    # currency = models.CharField(max_length=3, default="USD")


class Cupon(models.Model):
    cupon_code = models.CharField(max_length=50)    
    expired_date = models.DateTimeField()
    min_purchases = models.PositiveIntegerField()
    
    @property
    def status(self):
        return 'expire' if now() > self.expired_date else 'available'

class Discount(models.Model):
    seller = models.ForeignKey('user_shop.CustomUser', 
                               on_delete=models.CASCADE)  # Diskon tergantung seller
    discount_percentage = models.FloatField()
    min_purchases = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        return now() >= self.start_date and now() <= self.end_date



