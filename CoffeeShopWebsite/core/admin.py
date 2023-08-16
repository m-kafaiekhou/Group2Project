from django.contrib import admin
import django.apps

# Register your models here.


class MainAdminArea(admin.AdminSite) :
    site_header = 'Main Admin Area'
    login_template = 'core/admin/login.html'

main_site = MainAdminArea(name='MainAdmin')


class FilterCafeitem(admin.ModelAdmin) :
    list_display = ('name', 'is_available', 'price', 'category')
    list_filter = ('is_available', 'price')

