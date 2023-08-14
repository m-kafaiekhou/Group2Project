from django import forms


class OrderHistoryForm(forms.Form) :
    otp_code = forms.CharField(max_length=10)
    