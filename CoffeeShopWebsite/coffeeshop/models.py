from django.db import models
from django.db.models import Avg
from django.core.validators import RegexValidator
from staff.models import CustomUserModel


# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('c', 'Cancel'),
        ('a', 'accept'),
    )
    _REGEX = r'09(\d{9})$'
    phone_validator = RegexValidator(_REGEX, "The phone number provided is invalid")
    phone_number = models.CharField(
        'phone number', max_length=14, validators=[phone_validator],
        null=False
    )
    order_date = models.DateTimeField(auto_now_add=True)
    table_number = models.IntegerField(default=None)
    total_price = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)
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
    image = models.ImageField(upload_to="cafe_item/", default="preview-page0.jpg")
    is_available = models.BooleanField()
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    sub_category_fk = models.ForeignKey(
        "SubCategory", on_delete=models.SET_NULL, null=True
    )

    @property
    def item_rate(self):
        reviews = self.review_set
        rates = [rev.rating for rev in reviews]
        return sum(rates) / len(rates)

    @classmethod
    def top_rated_items(cls):
        return CafeItem.objects.annotate(item_rate=Avg("review_set__rating")).order_by(
                "-item_rate"
            )[:3]

    def category_name(self):
        return self.sub_category_fk.parent_category_fk


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
    image = models.ImageField(upload_to="parent_category", default="preview-page0.jpg")


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="sub_category", default="preview-page0.jpg")
    parent_category_fk = models.ForeignKey(
        ParentCategory,
        on_delete=models.CASCADE,
    )
