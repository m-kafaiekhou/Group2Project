from django import forms
from menus.models import CafeItem, Category
from orders.models import Order


class AddItemForm(forms.ModelForm):
    class Meta:
        model = CafeItem
        fields = "__all__"


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
