from django.contrib import admin
from .models import Order, OrderItem
from core.admin import main_site

# Register your models here.


main_site.register(Order)
main_site.register(OrderItem)
