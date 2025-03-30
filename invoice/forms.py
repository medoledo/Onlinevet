# forms.py
from django import forms
from .models import Invoice
from prices.models import Item
from django.forms.widgets import SelectDateWidget

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['category', 'item', 'quantity', 'discount', 'exp']

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['discount'].widget.attrs.update({'class': 'form-control'})
        self.fields['exp'].widget.attrs.update({'class': 'form-control'})

        categories = Item.objects.values_list('category', flat=True).distinct()
        self.fields['category'].choices = [(category, category) for category in categories]

    def get_items_by_category(self, category):
        return Item.objects.filter(category=category).all()

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        discount = cleaned_data.get('discount')

        if item and quantity is not None:
            price = item.price
            total_price = (price * quantity) - discount
            cleaned_data['price'] = price
            cleaned_data['total_price'] = total_price
            cleaned_data['exp'] = item.exp  # Set expiration date from item

        return cleaned_data



