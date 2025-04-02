from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
