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
    image = models.ImageField(upload_to="cafe_item/", blank=True, null=True)
    is_available = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    review = models.CharField(max_length=300)

    VERY_LOW = 1
    LOW = 2
    MIDDLE = 3
    HIGH = 4
    VERY_HIGH = 5
    RATING_COICES = (
        (VERY_LOW, 1),
        (LOW, 2),
        (MIDDLE, 3),
        (HIGH, 4),
        (VERY_HIGH, 5),
    )
    rating = models.IntegerField(choices=RATING_COICES, default=HIGH)


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="sub_category", blank=True, null=True)


class ParentCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="parent_category", blank=True, null=True)
