from django import forms
from .models import CustomUserModel


class CustomAuthenticationForm(forms.Form):
    phone_number = forms.CharField(max_length=14)
    registration_code = forms.CharField(max_length=4, widget=forms.PasswordInput())
    # class Meta:
    #     model = CustomUserModel
    #     fields = ('phone_number', 'password', )
