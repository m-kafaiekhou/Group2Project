from django import forms
from menus.models import CafeItem, Category


class AddItemForm(forms.ModelForm):
    class Meta:
        model = CafeItem
        fields = "__all__"


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
