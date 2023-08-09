from django.views import View
from django.shortcuts import render

from menus.models import CafeItem, Category
from orders.models import Order


class ItemListView(View):
    template_name = "staff/item_list.html"
    model_class = CafeItem

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class CategoryListView(View):
    pass


class ItemDetailView(View):
    pass


class CategoryDetailView(View):
    pass


class AddItemView(View):
    pass


class AddCategoryView(View):
    pass


class OrderListView(View):
    pass
