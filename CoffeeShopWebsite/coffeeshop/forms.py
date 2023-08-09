from django import forms
from django.forms import ModelForm
from .models import DynamicImages

class SearchMenu(forms.Form):
    search = forms.CharField()


class DynamicImageForm(ModelForm):
    class Meta:
        model = DynamicImages
        fields = "__all__"

