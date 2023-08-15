from django.contrib import admin
from .models import CafeItem, Category
# Register your models here.


admin.site.register(Category)
admin.site.register(CafeItem)
