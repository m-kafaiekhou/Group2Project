from django.db import models


# Create your models here.


class Order(models.Model):
    phone_number = models.CharField
    order_date = models.DateTimeField(auto_now_add=True)
    table_number = models.IntegerField(max_length=2, default=None)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)


class OrderItem(models.Model):
    quantity = models.IntegerField(max_length=4)


class CafeItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to="cafe-item/", blank=True, null=True)
    is_available = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    pass


class SubCategory(models.Model):
    pass


class ParentCategory(models.Model):
    pass
