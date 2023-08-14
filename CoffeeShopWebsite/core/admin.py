from django.contrib import admin
import django.apps
# Register your models here.
models = django.apps.apps.get_models()
class MainAdminArea(admin.AdminSite) :
    site_header = 'Main Admin Area'

main_site = MainAdminArea(name='MainAdmin')


