from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0


class FilterOrder(admin.ModelAdmin) :
    actions = ('cancel_order',)
    list_display = ('phone_number', 'status', 'order_date')
    list_filter = ('phone_number', 'status', 'table_number', 'order_date')
    inlines = [OrderItemInLine]

    def cancel_order(self, modeladmin, request, queryset):
        queryset.update(status='C')
    cancel_order.short_description = "Cancel Orders"

    def accept_order(self, modeladmin, request, queryset):
        queryset.update(status='A')
    accept_order.short_description = "Accept Orders"

    def draft_order(self, modeladmin, request, queryset):
        queryset.update(status='D')
    draft_order.short_description = "Draft Orders"


class FilterOrderItem(admin.ModelAdmin) :
    list_display = ('order','cafeitem' , 'quantity', 'price')
    list_filter = ('order', 'cafeitem')


admin.site.register(Order, FilterOrder)
admin.site.register(OrderItem, FilterOrderItem)
