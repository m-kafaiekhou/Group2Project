from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from menus.models import CafeItem, Category
from orders.models import Order


class ItemListView(LoginRequiredMixin, View):
    template_name = "staff/item_list.html"
    model_class = CafeItem

    def get(self, request, *args, **kwargs):
        items = self.model_class.objects.all()
        return render(request, self.template_name, context={'items': items})

    def post(self, request, *args, **kwargs):
        pass


class CategoryListView(View):
    template_name = "staff/category_list.html"
    model_class = Category

    def get(self, request, *args, **kwargs):
        categories = self.model_class.objects.all()
        return render(request, self.template_name, context={'categories': categories})

    def post(self, request, *args, **kwargs):
        pass


class ItemDetailView(View):
    template_name = "staff/item_detail.html"
    model_class = CafeItem


class CategoryDetailView(View):
    pass


class AddItemView(View):
    pass


class AddCategoryView(View):
    pass


class OrderListView(View):
    pass
