from django import forms
from .models import UserHours, UserProfile

class UserHoursForm(forms.ModelForm):
    class Meta:
        model = UserHours
        fields = ['user', 'arrival_time', 'left_time', 'total_hours']
        widgets = {
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'left_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),  # Use ModelChoiceField for selecting user
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all()  # Corrected to fetch users from UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }