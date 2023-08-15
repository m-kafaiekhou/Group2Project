from django.contrib import admin
from .models import Order, OrderItem
from core.admin import main_site

# Register your models here.


admin.site.register(Order)
admin.site.register(OrderItem)
