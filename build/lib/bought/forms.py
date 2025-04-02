from decimal import Decimal
from django import forms
from .models import Bought

class BoughtForm(forms.ModelForm):
    class Meta:
        model = Bought
        fields = ['item', 'price', 'quantity']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.total_price = Decimal(str(instance.quantity)) * instance.price  # Convert quantity to Decimal before multiplication
        if commit:
            instance.save()
        return instance
