from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count

# Local Imports
from menus.models import CafeItem, Category
from orders.models import Order, OrderItem
from . import forms
from .filters import ItemFilterSet, OrderFilterSet, CategoryFilterSet


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
    pass
