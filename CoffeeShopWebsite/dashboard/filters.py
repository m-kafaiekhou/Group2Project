from menus.models import CafeItem
import django_filters
from django import forms


class ItemFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Enter name'})
    )

    class Meta:
        model = CafeItem
        fields = ['name', 'category', 'is_available']
