from django.contrib import admin
from .models import CafeItem, Category
from core.admin import FilterCafeitem
# Register your models here.


admin.site.register(Category)
admin.site.register(CafeItem, FilterCafeitem)
