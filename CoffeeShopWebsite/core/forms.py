from django import forms
from django.core.validators import RegexValidator


class CustomUserLoginForm(forms.Form):
    _REGEX = r"09(\d{9})$"
    phone_validator = RegexValidator(_REGEX, "The phone number provided is invalid")

    phone_number = forms.CharField(max_length=14, validators=[phone_validator])


class VerifyCodeForm(forms.Form):
    verify_code = forms.IntegerField()
