from menus.models import CafeItem
from orders.models import Order
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


class OrderFilterSet(django_filters.FilterSet):
    phone_number = django_filters.CharFilter(
        field_name='phone_number',
        lookup_expr='startswith',
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    order_date = django_filters.DateFilter(
        field_name='order_date',
        lookup_expr='date',
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Order Date'})
    )
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=Order.Status.choices,
        empty_label='Select Status',
        widget=forms.Select(attrs={'placeholder': 'Status'})
    )

    class Meta:
        model = Order
        fields = ['phone_number', 'order_date', 'status']
