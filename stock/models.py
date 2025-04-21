from django.db import models
from users.models import User


class Wishlist(models.Model):
    symbol = models.CharField(max_length=255)
    current_price = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    price_wishlisted = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users')
    icon = models.URLField()

    def __str__(self):
        return self.symbol
