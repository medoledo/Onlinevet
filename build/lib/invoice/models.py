# models.py
from django.db import models
from prices.models import Item

class Invoice(models.Model):
    category = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.FloatField(default=1)  # Changed to FloatField
    discount = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    exp = models.DateField()

    def __str__(self):
        return f"Invoice #{self.id} - {self.item.name if self.item and not self.item.is_deleted else 'Deleted Item'} ({self.date})"
