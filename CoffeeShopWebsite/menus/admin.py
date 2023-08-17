from django.contrib import admin
from .models import CafeItem, Category
from core.admin import FilterCafeitem, FilterCategory
# Register your models here.


admin.site.register(Category, FilterCategory)
admin.site.register(CafeItem, FilterCafeitem)
