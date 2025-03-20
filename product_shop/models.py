# Django Library
from django.db import models

# Models from other apps
from user_shop.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    # Relation
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Product information
    name = models.CharField(max_length=1000)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField()
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # Additional information to handle unexpexted data 
    attributes = models.JSONField(default=dict, blank=True, null=True)

    # Update avg_rating value
    def update_avg_rating(self):
        reviews = self.reviews.all()
        result = reviews.aggregate(Avg("rating"))
        self.avg_rating = (
            result["avg_rating"] if result["avg_rating"] is not None else 0
        )
        self.save()

    def main_image(self):
        return self.images.filter(is_main=True).first()

    def __str__(self):
        return self.name

# Multiple Image 
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_shop/")
    is_main = models.BooleanField(default=False)

class Review(models.Model):
    # Relation
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "user_shop.CustomUser", related_name="review_users", on_delete=models.CASCADE
    )

    # Review information
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product} from {self.user}"
