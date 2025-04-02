# models.py
from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.FloatField()  # Changed to FloatField
    exp = models.DateField(default=datetime.date.today, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """Override the delete method to perform soft delete."""
        self.is_deleted = True
        self.save()
