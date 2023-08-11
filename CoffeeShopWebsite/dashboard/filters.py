from menus.models import CafeItem
import django_filters


class ItemFilterSet(django_filters.FilterSet):
    class Meta:
        model = CafeItem
        fields = ['category', 'is_available']
