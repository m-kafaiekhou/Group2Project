from django.contrib import admin
from menus.models import CafeItem, Category
from orders.models import Order, OrderItem
# Register your models here.
class MainAdminArea(admin.AdminSite) :
    site_header = 'Main Admin Area'

main_site = MainAdminArea(name='MainAdmin')