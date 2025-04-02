from django.db import models
from decimal import Decimal

class Bought(models.Model):
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.FloatField(default=1)  # Keeping it as FloatField
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_of_buying = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(str(self.quantity)) * self.price  # Ensure correct calculation
        super().save(*args, **kwargs)
