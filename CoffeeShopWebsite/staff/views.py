from django.views import View
from django.shortcuts import render

from menus.models import CafeItem, Category
from orders.models import Order


class ItemListView(View):
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
