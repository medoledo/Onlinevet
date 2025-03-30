from django import forms
from .models import Bird, Birddailyprice

class BirdForm(forms.ModelForm):
    bird_type = forms.ModelChoiceField(
        queryset=Birddailyprice.objects.all(),
        empty_label="Select Bird Type",
        widget=forms.Select(attrs={"class": "form-control"}),  # Adding the class here
        label="Bird Type",
    )

    class Meta:
        model = Bird
        fields = ['name', 'phone_number', 'bird_type', 'quantity', 'payed_money']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bird_type'].label_from_instance = lambda obj: obj.bird_type  # Show name instead of ID

class BirddailypriceForm(forms.ModelForm):
    class Meta:
        model = Birddailyprice
        fields = ['bird_type', 'bird_price']
