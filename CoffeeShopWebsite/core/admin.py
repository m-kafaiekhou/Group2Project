from django.contrib import admin
# Register your models here.
class MainAdminArea(admin.AdminSite) :
    site_header = 'Main Admin Area'

main_site = MainAdminArea(name='MainAdmin')
