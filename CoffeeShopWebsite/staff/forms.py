from django import forms
from menus.models import CafeItem


class AddItemForm(forms.ModelForm):
    class Meta:
        model = CafeItem
        fields = "__all__"
