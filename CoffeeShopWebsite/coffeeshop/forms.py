from django import forms

class SearchMenu(forms.Form):
    search = forms.CharField()
