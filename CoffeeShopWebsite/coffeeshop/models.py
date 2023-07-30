from django.db import models
from staff.models import CustomUserModel


# Create your models here.


class Order(models.Model):
    phone_number = models.CharField
    order_date = models.DateTimeField(auto_now_add=True)
    table_number = models.IntegerField(default=None)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    staff_fk = models.ForeignKey(
        CustomUserModel,
        on_delete=models.SET_NULL,
        null=True,
    )


class OrderItem(models.Model):
    quantity = models.IntegerField()
    order_fk = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    cafeitem_fk = models.ForeignKey(
        "CafeItem",
        on_delete=models.CASCADE,
    )


class CafeItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to="cafe_item/", blank=True, null=True)
    is_available = models.BooleanField()
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    sub_category_fk = models.ForeignKey(
        "SubCategory", on_delete=models.SET_NULL, null=True
    )


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

    cafeitem_fk = models.ForeignKey(
        CafeItem,
        on_delete=models.CASCADE,
    )


class ParentCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="parent_category", blank=True, null=True)


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="sub_category", blank=True, null=True)
    parent_dategory_fk = models.ForeignKey(
        ParentCategory,
        on_delete=models.CASCADE,
    )
