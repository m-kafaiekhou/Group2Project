from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0


class FilterOrder(admin.ModelAdmin) :
    list_display = ('phone_number', 'status', 'order_date')
    list_filter = ('phone_number', 'status')
    inlines = [
        OrderItemInLine
    ]


class FilterOrderItem(admin.ModelAdmin) :
    list_display = ('order','cafeitem' , 'quantity', 'price')
    list_filter = ('order', 'cafeitem')


admin.site.register(Order, FilterOrder)
admin.site.register(OrderItem, FilterOrderItem)
