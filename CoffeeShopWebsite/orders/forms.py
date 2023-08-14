from django import forms


class OrderHistoryForm(forms.Form) :
    phone_number = forms.CharField(max_length=20)
    