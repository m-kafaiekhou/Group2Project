from django import forms
from .models import CustomUserModel


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=14)


class OtpForm(forms.Form):
    registration_code = forms.CharField(max_length=4, widget=forms.PasswordInput())
