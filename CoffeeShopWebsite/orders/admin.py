from django.contrib import admin
from .models import Order, OrderItem
from core.admin import FilterOrder, FilterOrderItem

# Register your models here.


admin.site.register(Order, FilterOrder)
admin.site.register(OrderItem, FilterOrderItem)
