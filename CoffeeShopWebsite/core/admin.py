from django.contrib import admin
import django.apps

# Register your models here.


class MainAdminArea(admin.AdminSite) :
    site_header = 'Main Admin Area'
    login_template = 'core/admin/login.html'

main_site = MainAdminArea(name='MainAdmin')


class FilterCafeitem(admin.ModelAdmin) :
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter = ('is_available', 'price')

class FilterCategory(admin.ModelAdmin) :
    list_display = ('name', 'parent_category')

class FilterOrder(admin.ModelAdmin) :
    list_display = ('phone_number', 'status', 'order_date')
