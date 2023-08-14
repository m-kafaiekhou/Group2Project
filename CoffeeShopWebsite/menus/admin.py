from django.contrib import admin
from .models import CafeItem, Category
from core.admin import main_site
# Register your models here.


main_site.register(Category)
main_site.register(CafeItem)
