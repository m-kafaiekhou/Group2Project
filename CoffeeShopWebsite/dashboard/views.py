from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.http import JsonResponse

from menus.models import CafeItem, Category
from orders.models import Order, OrderItem
from . import forms
from .filters import ItemFilterSet, OrderFilterSet
from django.db.models.functions import ExtractHour, ExtractDay, ExtractWeek, ExtractMonth, ExtractYear
from django.db.models import Count, F, Sum, Avg
from .chart_utils import year_dict, months, month_dict, month, day_dict, day
from datetime import datetime

class ItemListView(LoginRequiredMixin, View):
    template_name = "dashboard/item_list.html"
    model_class = CafeItem

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        items = self.model_class.objects.all()
        filter_set = ItemFilterSet(data, items)

        order_by = data.get('orderby', 'df')
        if order_by == 'df':
            query_set = filter_set.qs.order_by('name')
        elif order_by == 'mo':
            query_set = filter_set.qs.order_by('-price')
        elif order_by == 'le':
            query_set = filter_set.qs.order_by('price')
        else:
            query_set = filter_set.qs
        paginator = Paginator(query_set, 2)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'filter_set': filter_set,
            'name': data.get('name', ''),
            'category': data.get('category', ''),
            'is_available': data.get('is_available', ''),
            'orderby': order_by,
        }

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
    template_name = "dashboard/order_list.html"
    model_class = Order

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        items = self.model_class.objects.all()
        filter_set = ItemFilterSet(data, items)

        order_by = data.get('orderby', 'df')
        # if order_by == 'df':
        #     query_set = filter_set.qs.order_by('name')
        # elif order_by == 'mo':
        #     query_set = filter_set.qs.order_by('-price')
        # elif order_by == 'le':
        #     query_set = filter_set.qs.order_by('price')
        # else:
        query_set = filter_set.qs
        paginator = Paginator(query_set, 2)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'filter_set': filter_set,
            'name': data.get('name', ''),
            'category': data.get('category', ''),
            'is_available': data.get('is_available', ''),
            'orderby': order_by,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pass


class DashboardView(View):
    template_view = "dashboard/dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_view)




# ********************************* Chart Area ********************************* #

def year_filter_options(request):
    grouped_orders = Order.objects.annotate(year=ExtractYear("order_date")).values("year").order_by("-year").distinct()
    options = [order["year"] for order in grouped_orders]

    return JsonResponse({
        "options":options,
    })


def month_filter_options(request):
    grouped_orders = Order.objects.annotate(day=ExtractMonth("order_date")).values("day").order_by("-day").distinct()
    options = [order["day"] for order in grouped_orders]

    return JsonResponse({
        "options":options,
    })


def day_filter_options(request):
    grouped_orders = Order.objects.annotate(hour=ExtractHour("order_date")).values("hour").order_by("-hour").distinct()
    options = [order["hour"] for order in grouped_orders]

    return JsonResponse({
        "options":options,
    })


def yearly_sales_chart(request, year):
    this_year = 
    orders = OrderItem.objects.filter(order__order_date__year=year)
    grouped_orders = orders.annotate(p=F("price")).annotate(month=ExtractMonth("order__order_date"))\
        .values("month").annotate(total=Sum("price")).values("month","total").order_by("month")
    
    sale_dict = year_dict()

    for group in grouped_orders:
        sale_dict[months[group["month"]-1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                "data": list(sale_dict.values()),
            }]
        }
    })


def monthly_sales_chart(request, day):
    orders = OrderItem.objects.filter(order__order_date__day=day)
    grouped_orders = orders.annotate(p=F("price")).annotate(day=ExtractDay("order__order_date"))\
        .values("day").annotate(total=Sum("price")).values("day","total").order_by("day")
    
    sale_dict = month_dict()

    for group in grouped_orders:
        sale_dict[month[group["day"]-1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Sales in {day}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                "data": list(sale_dict.values()),
            }]
        }
    })

def daily_sales_chart(request, hour):
    orders = OrderItem.objects.filter(order__order_date__hour=hour)
    grouped_orders = orders.annotate(p=F("price")).annotate(hour=ExtractHour("order__order_date"))\
        .values("hour").annotate(total=Sum("price")).values("hour","total").order_by("hour")
    
    sale_dict = day_dict()

    for group in grouped_orders:
        sale_dict[day[group["hour"]-1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Sales in {hour}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                "data": list(sale_dict.values()),
            }]
        }
    })