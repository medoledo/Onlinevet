# forms.py
from django import forms
from .models import Item, Category

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'price', 'quantity', 'exp']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Item Name'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Price'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Quantity'})
        self.fields['exp'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Expiration Date'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Category Name'})
