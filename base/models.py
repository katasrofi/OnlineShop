from django.db import models


# Create your models here.
class Wishlist(models.Model):
    # Composite key
    user_id = models.ForeignKey(
        "user_shop.CustomUser", related_name="user_wishlists", on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        "product_shop.Product",
        related_name="product_wishlists",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
