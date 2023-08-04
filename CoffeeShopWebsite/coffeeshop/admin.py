from django.contrib import admin
from .models import Order, OrderItem, CafeItem, Review, Category

# Register your models here.


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CafeItem)
admin.site.register(Review)
admin.site.register(Category)
