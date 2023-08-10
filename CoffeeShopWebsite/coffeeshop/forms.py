from django import forms
from django.forms import ModelForm
from .models import DynamicImages, DynamicTexts, DynamicNumbers

class SearchMenu(forms.Form):
    search = forms.CharField()


class DynamicImageForm(ModelForm):
    class Meta:
        model = DynamicImages
        fields = "__all__"


class DynamicTextForm(ModelForm):
    class Meta:
        model = DynamicTexts
        fields = "__all__"


class DynamicNumberForm(ModelForm):
    class Meta:
        model = DynamicNumbers
        fields = "__all__"