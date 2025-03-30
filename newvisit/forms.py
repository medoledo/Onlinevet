from django import forms
from .models import Visit, Owner

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['owner', 'age', 'weight_in_kg', 'diagnosis', 'treatment', 'visit_date', 'next_check_date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up the 'owner' field to fetch all owners
        self.fields['owner'].queryset = Owner.objects.all()

        # Auto-fill pet details when owner is selected
        self.fields['pet_name'] = forms.CharField(
            widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            required=False
        )
        self.fields['pet_type'] = forms.CharField(
            widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            required=False
        )
        self.fields['sex'] = forms.CharField(
            widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            required=False
        )

    class Media:
        js = ('js/update_owner_details.js',)  # JS to auto-fill fields when owner is selected
