from django.contrib import admin
import django.apps
# Register your models here.


# admin.site.unregister(django.contrib.sessions.models.Session)

class MainAdminArea(admin.AdminSite) :
    site_header = 'Main Admin Area'
    login_template = 'core/admin/login.html'


main_site = MainAdminArea(name='MainAdmin')

