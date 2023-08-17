from django.contrib import admin
import django.apps

# Register your models here.


# admin.site.unregister(django.contrib.sessions.models.Session)

class MainAdminArea(admin.AdminSite):
    site_header = 'Main Admin Area'
    login_template = 'core/admin/login.html'

main_site = MainAdminArea(name='MainAdmin')


class FilterCafeitem(admin.ModelAdmin) :
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter = ('is_available', )
    list_per_page = 15
    def make_cafeitems_unavailable(self, modeladmin,request, queryset):
        queryset.update(is_available=False)
    make_cafeitems_unavailable.short_description = "Marks elected Cafe Items as unavailable"

    

class FilterCategory(admin.ModelAdmin) :
    list_display = ('name', 'parent_category')
    list_filter = ('parent_category',)
    list_per_page = 15

