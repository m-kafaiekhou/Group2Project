# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

#
#
# class CustomAuthenticationForm(AuthenticationForm):
#     phone_number = forms.CharField(widget=forms.TextInput)
#
#     class Meta:
#         fields = ['phone_number', 'password']


class CustomUserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=14)

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
