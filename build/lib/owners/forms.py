# owners/forms.py
from django import forms
from .models import Owner , PetType

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'phone_number', 'pet_name', 'pet_type', 'sex']

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Owner Name'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone Number'})
        self.fields['pet_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Pet Name'})
        self.fields['pet_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['sex'].widget.attrs.update({'class': 'form-select'})


class PetTypeForm(forms.ModelForm):
    class Meta:
        model = PetType
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(PetTypeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Pet Type Name'})