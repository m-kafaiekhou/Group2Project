from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict

from menus.models import CafeItem, Category
from orders.models import Order
from . import forms
from .filters import ItemFilterSet


class ItemListView(LoginRequiredMixin, View):
    template_name = "dashboard/item_list.html"
    model_class = CafeItem

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        items = self.model_class.objects.all()
        filter_set = ItemFilterSet(data, items)
        context = {
            'items': filter_set.qs,
            'filter_set': filter_set,
        }
        print([i for i in filter_set.form])
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pass


class CategoryListView(LoginRequiredMixin, View):
    template_name = "staff/category_list.html"
    model_class = Category

    def get(self, request, *args, **kwargs):
        categories = self.model_class.objects.all()
        return render(request, self.template_name, context={'categories': categories})

    def post(self, request, *args, **kwargs):
        pass


class ItemDetailView(LoginRequiredMixin, View):
    template_name = "staff/item_detail.html"
    model_class = CafeItem
    form_class = forms.AddItemForm

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(self.model_class, pk=kwargs["pk"])
        initial_data = model_to_dict(item, fields=[field.name for field in item._meta.fields])
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, context={'item': item, 'form': form})

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(self.model_class, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=item)

        if form.is_valid():
            form.save()

        redirect('item_detail', kwargs['pk'])


class CategoryDetailView(LoginRequiredMixin, View):
    template_name = "staff/category_detail.html"
    model_class = Category
    form_class = forms.AddCategoryForm

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(self.model_class, pk=kwargs["pk"])
        initial_data = model_to_dict(item, fields=[field.name for field in item._meta.fields])
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, context={'item': item, 'form': form})

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(self.model_class, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=item)

        if form.is_valid():
            form.save()

        redirect('category_detail', kwargs['pk'])


class AddItemView(LoginRequiredMixin, View):
    template_name = "staff/item_add.html"
    model_class = CafeItem
    form_class = forms.AddItemForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return redirect('add_item')


class AddCategoryView(LoginRequiredMixin, View):
    template_name = "staff/category_add.html"
    model_class = Category
    form_class = forms.AddCategoryForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return redirect('add_category')


class OrderDetailView(LoginRequiredMixin, View):
    template_name = "staff/order_detail.html"
    model_class = Order
    form_class = forms.OrderUpdateForm

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(self.model_class, pk=kwargs["pk"])
        initial_data = model_to_dict(item, fields=[field.name for field in item._meta.fields])
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, context={'order': item, 'form': form})

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(self.model_class, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=item)

        if form.is_valid():
            form.save()

        return redirect('order_list')


class OrderListView(LoginRequiredMixin, View):
    template_name = "staff/order_list.html"
    model_class = Order

    def get(self, request, *args, **kwargs):
        orders = self.model_class.objects.all().order_by('-status')
        return render(request, self.template_name, context={'orders': orders})

    def post(self, request, *args, **kwargs):
        pass
