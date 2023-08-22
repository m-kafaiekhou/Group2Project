from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.http import JsonResponse


# Local Imports
from menus.models import CafeItem, Category
from orders.models import Order, OrderItem
from . import forms
from .filters import ItemFilterSet, OrderFilterSet, CategoryFilterSet

from django.db.models.functions import ExtractHour, ExtractDay, ExtractWeek, ExtractMonth, ExtractYear, Extract
from django.db.models import Count, F, Sum, Avg
from .chart_utils import year_dict, months, month_dict, month, day_dict, day
from datetime import datetime
from collections import defaultdict


class ItemListView(LoginRequiredMixin, View):
    template_name = "dashboard/item_list.html"
    model_class = CafeItem
    filter_class = ItemFilterSet

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        items = self.model_class.objects.all()
        filter_set = self.filter_class(data, items)

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
    template_name = "dashboard/category_list.html"
    model_class = Category
    filter_class = CategoryFilterSet

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        items = self.model_class.objects.all()
        filter_set = self.filter_class(data, items)

        order_by = data.get('orderby', 'df')
        if order_by == 'df':
            query_set = filter_set.qs.order_by('name')
        elif order_by == 'mo':
            query_set = filter_set.qs.annotate(sale_count=Count('cafeitem__orderitem')).order_by('-sale_count')
        elif order_by == 'le':
            query_set = filter_set.qs.annotate(sale_count=Count('cafeitem__orderitem')).order_by('sale_count')
        else:
            query_set = filter_set.qs

        paginator = Paginator(query_set, 2)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'filter_set': filter_set,
            'name': data.get('name', ''),
            'orderby': order_by,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pass


class ItemDetailView(LoginRequiredMixin, View):
    template_name = "dashboard/item_detail.html"
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
    template_name = "dashboard/category_detail.html"
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
    template_name = "dashboard/order_detail.html"
    model_class = Order
    form_class = forms.OrderUpdateForm

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(self.model_class, pk=kwargs["pk"])
        initial_data = model_to_dict(item, fields=[field.name for field in item._meta.fields])
        form = self.form_class(initial=initial_data)
        cafeitems = CafeItem.objects.all()

        context = {
            'order': item,
            'form': form,
            'cafeitems': cafeitems
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if "quantity" in request.POST:
            quantity = request.POST.get('quantity')
            item = request.POST.get('item')

            if item.isdigit() and quantity.isdigit():
                OrderItem.objects.create(order_id=kwargs['pk'], cafeitem_id=item, quantity=int(quantity))

        else:
            item = get_object_or_404(self.model_class, pk=kwargs['pk'])
            form = self.form_class(request.POST, instance=item)

            if form.is_valid():
                item = form.save(commit=False)
                item.staff = request.user
                item.save()

        return redirect('order_details', kwargs["pk"])


class OrderItemUpdateView(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        order_item_id = request.POST.get('orderitem')
        quantity = request.POST.get('quantity')
        order_item = get_object_or_404(OrderItem, pk=int(order_item_id))

        order_item.quantity = int(quantity)
        order_item.save()

        return redirect('order_details', order_id)


class OrderListView(LoginRequiredMixin, View):
    template_name = "dashboard/order_list.html"
    model_class = Order
    filter_class = OrderFilterSet

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        items = self.model_class.objects.all()
        filter_set = self.filter_class(data, items)

        order_by = data.get('orderby', 'df')

        if order_by == 'df':
            query_set = filter_set.qs.order_by('order_date')
        elif order_by == 'mo':
            query_set = filter_set.qs.order_by('orderitem__price')
        elif order_by == 'le':
            query_set = filter_set.qs.order_by('-orderitem__price')

        paginator = Paginator(query_set, 2)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'filter_set': filter_set,
            'phone_number': data.get('phone_number', ''),
            'order_date': data.get('order_date', ''),
            'status': data.get('status', ''),
            'orderby': order_by,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('itemId', None)
        status = kwargs['stat']
        try:
            order = self.model_class.objects.get(pk=pk)
            order.status = status
            order.staff = request.user
            order.save()
            return JsonResponse({'message': 'Order status updated successfully'})

        except self.model_class.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class DashboardView(View):
    template_view = "dashboard/dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_view)


# ************************************************* Chart Area ************************************************* #

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


def yearly_sales_chart(request):
    this_year = datetime.now().year
    orders = OrderItem.objects.filter(order__order_date__year=this_year)
    grouped_orders = orders.annotate(p=F("price")).annotate(month=ExtractMonth("order__order_date"))\
        .values("month").annotate(total=Sum("price")).values("month","total").order_by("month")
    
    sale_dict = year_dict()

    for group in grouped_orders:
        sale_dict[months[group["month"]-1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Sales in {this_year}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def monthly_sales_chart(request):
    month = datetime.now().month
    month_name = datetime.now().strftime("%B")
    orders = OrderItem.objects.filter(order__order_date__month=month)
    grouped_orders = orders.annotate(p=F("price")).annotate(day=ExtractDay("order__order_date"))\
        .values("day").annotate(total=Sum("price")).values("day","total").order_by("day")
    
    sale_dict = month_dict()

    for group in grouped_orders:
        sale_dict[day[group["day"]-1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Sales in {month_name}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def daily_sales_chart(request):
    today = datetime.now().day
    orders = OrderItem.objects.filter(order__order_date__day=today)
    grouped_orders = orders.annotate(p=F("price")).annotate(hour=ExtractHour("order__order_date"))\
        .values("hour").annotate(total=Sum("price")).values("hour","total").order_by("hour")
    
    sale_dict = day_dict()

    for group in grouped_orders:
        sale_dict[day[group["hour"]-1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Sales in Today",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def sales_by_time_of_day(request):
    '''
    Chart view function to get the amount of sale between two seprate times
    In a day in this month.
    st_date = the start of date yyyy/mm/dd
    nd_date = the end of date yyyy/mm/dd
    
    '''
    date1 = request.GET.get("start_date", None)
    date2 = request.GET.get("end_date", None)
    
    if date1 and date2 == None:
        st_date = None
        nd_date = None
    elif date1 == None:
        st_date = None
        nd_date = date2
    elif date2 == None:
        st_date = date1
        nd_date = None
    elif date2 > date1:
        st_date = date1
        nd_date = date2
    elif date1 > date2:
        st_date = date2
        nd_date = date1


    if st_date and nd_date:
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=nd_date,
        )
    elif nd_date == None:
        today = datetime.now().date()
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=today,
        )
    elif st_date == None:
        orders = OrderItem.objects.filter(
            order__order_date__date=nd_date, 
        )
    elif (st_date and nd_date == None):
        today = datetime.now().date()
        orders = OrderItem.objects.filter(
            order__order_date__date=today, 
        )

    time_sales = orders.annotate(p=F("price")).annotate(hour=ExtractHour("order__order_date"))\
        .values("hour").annotate(total=Sum("price")).values("order__order_date__date" ,"hour" ,"total")

    
    new_list = list()
    for d in time_sales:
        new_dict = {"datetime":str(d["order__order_date__date"])+ " " + str(d["hour"])+":00:00", "total": d["total"]}
        new_list.append(new_dict)
    

    new_dicts = defaultdict(int)
    for d in new_list:
        new_dicts[d["datetime"]] += int(d["total"])

    date_list = [{"datetime": date, "total":price} for date, price in new_dicts.items()]
    sorted_date_list = sorted(date_list, key=lambda x: x["total"], reverse=True)

    sale_dict = dict()
    for d in sorted_date_list:
        sale_dict[d["datetime"]] = round(d["total"], 2)


    return JsonResponse({
        "title": f"Sales by Time of Day Between {st_date} and {nd_date}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def total_sales(request):
    date1 = request.GET.get("start_date", None)
    date2 = request.GET.get("end_date", None)
    
    if date1 and date2 == None:
        st_date = None
        nd_date = None
    elif date1 == None:
        st_date = None
        nd_date = date2
    elif date2 == None:
        st_date = date1
        nd_date = None
    elif date2 > date1:
        st_date = date1
        nd_date = date2
    elif date1 > date2:
        st_date = date2
        nd_date = date1

    if st_date and nd_date:
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=nd_date,
            )
    elif nd_date == None:
        now = datetime.now()
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=now,
            )
    elif st_date == None:
        orders = OrderItem.objects.filter(
            order__order_date__date=nd_date, 
            )
    elif st_date and nd_date == None:
        orders = OrderItem.objects.all()
    
    all_orders_in_range = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("total")
    
    total = 0
    for order in all_orders_in_range:
        total += order["total"]

    return JsonResponse({
        "title": f"Total Sales Between {st_date} and {nd_date}",
        "data": {
            "labels": ["total"],
            "datasets": [{
                "label": "Amount (T)",
                "data": [total],
            }]
        }
    })


def top_10_selling_items(request): # year, month, day
    date1 = request.GET.get("start_date", None)
    date2 = request.GET.get("end_date", None)
    
    if date1 and date2 == None:
        st_date = None
        nd_date = None
    elif date1 == None:
        st_date = None
        nd_date = date2
    elif date2 == None:
        st_date = date1
        nd_date = None
    elif date2 > date1:
        st_date = date1
        nd_date = date2
    elif date1 > date2:
        st_date = date2
        nd_date = date1

    if st_date and nd_date:
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=nd_date,
            )
    elif nd_date == None:
        now = datetime.now()
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=now,
            )
    elif st_date == None:
        orders = OrderItem.objects.filter(
            order__order_date__date=nd_date, 
            )
    elif st_date and nd_date == None:
        orders = OrderItem.objects.all()


    all_items = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("cafeitem__name", "total")

    new_dict = defaultdict(int)
    for d in all_items:
        new_dict[d["cafeitem__name"]] += int(d["total"])
    
    chart_items = [{"cafeitem__name":name, "total": price} for name, price in new_dict.items()]
    sorted_chart_items = sorted(chart_items,key=lambda x: x["total"], reverse=True)

    top_items = list()
    for d in sorted_chart_items:
        if len(top_items) < 10:
            top_items.append(d)
    
    
    sale_dict = dict()
    for i in top_items:
        sale_dict[i["cafeitem__name"]] = round(i["total"], 2)

    return JsonResponse({
        "title": f"Top 10 Best Sellers",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def top_10_customers(requests):
    orders = OrderItem.objects.all()
    all_numbers = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("order__phone_number", "total")

    new_dict = defaultdict(int)
    for d in all_numbers:
        new_dict[d["order__phone_number"]] += int(d["total"])

    chart_ph_numbers = [{"order__phone_number": number, "total":price} for number, price in new_dict.items()]
    sorted_ph_numbers = sorted(chart_ph_numbers, key=lambda x: x["total"], reverse=True)

    top_customers = list()
    for d in sorted_ph_numbers:
        if len(top_customers) < 10:
            top_customers.append(d)

    sale_dict = dict()
    for d in top_customers:
        sale_dict[d["order__phone_number"]] = round(d["total"], 2)

    return JsonResponse({
        "title": "Top 10 Best Customers",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def sales_by_category(requests):
    orders = OrderItem.objects.all()
    all_caterories = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("cafeitem__category__name", "total")

    new_dict = defaultdict(int)
    for d in all_caterories:
        new_dict[d["cafeitem__category__name"]] += int(d["total"])

    chart_category = [{"cafeitem__category__name": name, "total":price} for name, price in new_dict.items()]
    sorted_category = sorted(chart_category, key=lambda x: x["total"], reverse=True)

    sale_dict = dict()
    for d in sorted_category:
        sale_dict[d["cafeitem__category__name"]] = round(d["total"], 2)

    return JsonResponse({
        "title": "Category Sales",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def sales_by_employee(request): # Table, or a bar Chart.
    date1 = request.GET.get("start_date", None)
    date2 = request.GET.get("end_date", None)
    
    if date1 and date2 == None:
        st_date = None
        nd_date = None
    elif date1 == None:
        st_date = None
        nd_date = date2
    elif date2 == None:
        st_date = date1
        nd_date = None
    elif date2 > date1:
        st_date = date1
        nd_date = date2
    elif date1 > date2:
        st_date = date2
        nd_date = date1

    if st_date and nd_date:
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=nd_date,
        )
    elif nd_date == None:
        today = datetime.now().date()
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=today,
        )
    elif st_date == None:
        orders = OrderItem.objects.filter(
            order__order_date__date=nd_date, 
        )
    elif (st_date and nd_date == None):
        today = datetime.now().date()
        orders = OrderItem.objects.filter(
            order__order_date__date=today, 
        )

    all_staff = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("order__staff__first_name", "order__staff__last_name", "total")
    
    new_list = list()
    for d in all_staff:
        new_dict = {"staff_name":d["order__staff__first_name"]+ " " + d["order__staff__last_name"], "total": d["total"]}
        new_list.append(new_dict)
    
    new_dicts = defaultdict(int)
    for d in new_list:
        new_dicts[d["staff_name"]] += int(d["total"])

    staff_list = [{"staff_name": name, "total":price} for name, price in new_dicts.items()]
    sorted_staff_list = sorted(staff_list, key=lambda x: x["total"], reverse=True)
    print(sorted_staff_list)

    sale_dict = dict()
    for d in sorted_staff_list:
        sale_dict[d["staff_name"]] = round(d["total"], 2)

    
    return JsonResponse({
        "title": "Employee Sales",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def peak_business_hour(request):
    orders = OrderItem.objects.all()
    grouped_orders = orders.annotate(p=F("price")).annotate(hour=ExtractHour("order__order_date"))\
        .values("hour").annotate(total=Sum("price")).values("hour","total").order_by("hour")
    
    sale_dict = day_dict()

    for group in grouped_orders:
        sale_dict[day[group["hour"]-1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Peak Business Hour Sales",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def most_popular_items(request):
    orders = OrderItem.objects.all()
    all_items = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("cafeitem__name", "total")

    new_dict = defaultdict(int)
    for d in all_items:
        new_dict[d["cafeitem__name"]] += int(d["total"])
    
    chart_items = [{"cafeitem__name":name, "total": price} for name, price in new_dict.items()]
    sorted_chart_items = sorted(chart_items,key=lambda x: x["total"], reverse=True)

    top_items = list()
    for d in sorted_chart_items:
        if len(top_items) < 10:
            top_items.append(d)
    
    
    sale_dict = dict()
    for i in top_items:
        sale_dict[i["cafeitem__name"]] = round(i["total"], 2)

    return JsonResponse({
        "title": "Most Popular Items(All Time)",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                'borderColor': '#d048b6',
                'borderWidth': 2,
                'borderDash': [],
                'borderDashOffset': 0.0,
                'pointBackgroundColor': '#d048b6',
                'pointBorderColor': 'rgba(255,255,255,0)',
                'pointHoverBackgroundColor': '#d048b6',
                'pointBorderWidth': 20,
                'pointHoverRadius': 4,
                'pointHoverBorderWidth': 15,
                'pointRadius': 4,
                "data": list(sale_dict.values()),
            }]
        }
    })


def order_status_report(request):  # Table, not a Chart. status= "D", "C", "A"
    date1 = request.GET.get("start_date", None)
    date2 = request.GET.get("end_date", None)
    status = request.GET.get("status", None)

    if date1 and date2 == None:
        st_date = None
        nd_date = None
    elif date1 == None:
        st_date = None
        nd_date = date2
    elif date2 == None:
        st_date = date1
        nd_date = None
    elif date2 > date1:
        st_date = date1
        nd_date = date2
    elif date1 > date2:
        st_date = date2
        nd_date = date1

    if status == None:
        return JsonResponse({
        "title": f"No Data",
        "data": {
            "labels": [],
            "datasets": [{
                "label": "Amount (T)",
                "data": [],
            }]
        }
    })

    if st_date and nd_date:
        orders = Order.objects.filter(
            order_date__date__gt=st_date, 
            order_date__date__lt=nd_date, 
            status=status,
            )
    elif nd_date == None:
        today = datetime.now().date()
        orders = Order.objects.filter(
            order_date__date__gt=st_date, 
            order_date__date__lt=today, 
            status=status,
            )
    elif st_date == None:
        orders = Order.objects.filter( 
            order_date__date=nd_date, 
            status=status,
            )
    elif (st_date and nd_date == None):
        today = datetime.now().date()
        orders = Order.objects.filter(
            order_date__date=today, 
            status=status,
            )

    
    grouped_orders = orders.annotate(p=F("status")).annotate(count=Count("status")).values("status","count").order_by("-count")

    sale_dict = dict()

    for group in grouped_orders:
        sale_dict[group["status"]] = group["count"]

    return JsonResponse({
        "title": f"Order Status Count between {st_date} and {nd_date}",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                "data": list(sale_dict.values()),
            }]
        }
    })


def customer_order_history(request):
    '''
    Returns a context of data(customer_orderitem_data, customer_order_data) to 
    The dashboard template using render method.
    st_date = the start of date yyyy/mm/dd
    nd_date = the end of date yyyy/mm/dd
    phone = the customer phone number(order__phone_number).
    '''
    date1 = request.GET.get("start_date", None)
    date2 = request.GET.get("end_date", None)
    phone = request.GET.get("phone_number", None)

    if date1 and date2 == None:
        st_date = None
        nd_date = None
    elif date1 == None:
        st_date = None
        nd_date = date2
    elif date2 == None:
        st_date = date1
        nd_date = None
    elif date2 > date1:
        st_date = date1
        nd_date = date2
    elif date1 > date2:
        st_date = date2
        nd_date = date1

    if phone == None:
        context = {
        "customer_orderitem_data":"",
        "customer_order_data":"",
        }
        return render(request, "", context)
    

    if st_date and nd_date:
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=nd_date,
            order__phone_number=phone,
        )
    elif nd_date == None:
        today = datetime.now().date()
        orders = OrderItem.objects.filter(
            order__order_date__date__gt=st_date, 
            order__order_date__date__lt=today,
            order__phone_number=phone,
        )
    elif st_date == None:
        orders = OrderItem.objects.filter(
            order__order_date__date=nd_date,
            order__phone_number=phone, 
        )
    elif (st_date and nd_date == None):
        today = datetime.now().date()
        orders = OrderItem.objects.filter(
            order__order_date__date=today, 
            order__phone_number=phone,
        )

    if st_date and nd_date:
        order_data = Order.objects.filter(
            order_date__date__gt=st_date, 
            order_date__date__lt=nd_date, 
            phone_number=phone,
            )
    elif nd_date == None:
        today = datetime.now().date()
        order_data = Order.objects.filter(
            order_date__date__gt=st_date, 
            order_date__date__lt=today, 
            phone_number=phone,
            )
    elif st_date == None:
        order_data = Order.objects.filter( 
            order_date_date=nd_date, 
            phone_number=phone,
            )
    elif (st_date and nd_date == None):
        today = datetime.now().date()
        order_data = Order.objects.filter(
            order_date__date=today, 
            phone_number=phone,
            )
    
    context = {
        "customer_orderitem_data":orders,
        "customer_order_data":order_data,
        }
    return render(request, "", context)



# ************************************************* Customer Demographic ************************************************* #

def total_money_spent(request):
    phone = request.GET.get("phone_number", None)

    if not phone:
        context = {}
        return render(request, "", context)

    orders = OrderItem.objects.filter(
        order__phone_number=phone 
        )
    
    all_orders = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("total")
    
    total = 0
    for order in all_orders:
        total += order["total"]

    context = {"total":total}
    return render(request, "", context)


def average_money_spent(request): # Not Done
    phone = request.GET.get("phone_number", None)
    
    if not phone:
        context = {}
        return render(request, "", context)

    orders = OrderItem.objects.filter(
        order__phone_number=phone 
        )
    
    all_orders = orders.annotate(p=F("price")).annotate(total=Sum("price")).values("total")

    average = 0
    for order in all_orders:
        average += order["total"]

    average = average / len(all_orders)

    context = {"total":average}
    return render(request, "", context)


def number_of_items_bought(request):
    phone = request.GET.get("phone_number", None)

    if not phone:
        return JsonResponse({
        "title": f"No Data Found",
        "data": {
            "labels": [],
            "datasets": [{
                "label": "Amount (T)",
                "data": [],
            }]
        }
    })

    orders = OrderItem.objects.filter(
        order__phone_number=phone 
        )
    
    all_orders = orders.annotate(p=F("quantity")).annotate(total=Sum("quantity")).values("cafeitem__name" ,"total")

    sale_dict = dict()

    for order in all_orders:
        sale_dict[order["cafeitem__name"]] = order["total"]

    return JsonResponse({
        "title": f"Number of Each Item Bought By Customer",
        "data": {
            "labels": list(sale_dict.keys()),
            "datasets": [{
                "label": "Amount (T)",
                "data": list(sale_dict.values()),
            }]
        }
    })


def favorite_item(request):
    pass


def favorite_category(request):
    pass


def days_customer_went_to_coffeeshop(request):
    pass


def customer_rating(request):
    pass

