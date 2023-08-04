from django.db import models
from django.db.models import Avg
from django.core.validators import RegexValidator
from staff.models import CustomUserModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


def regex_validation():
    _REGEX = r"09(\d{9})$"
    phone_validator = RegexValidator(_REGEX, "The phone number provided is invalid")


class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = "D", _("Draft")
        CANCEL = "C", _("Cancel")
        ACCEPT = "A", _("Accept")

    status = models.CharField(choices=Status.choices, max_length=1)

    regex = regex_validation()
    phone_number = models.CharField(
        "phone number", max_length=14, validators=[regex], null=False
    )
    order_date = models.DateTimeField(auto_now_add=True)
    table_number = models.IntegerField(default=None)
    staff = models.ForeignKey(
        CustomUserModel,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return self.phone_number


class OrderItem(models.Model):
    order_fk = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    cafeitem_fk = models.ForeignKey(
        "CafeItem",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()
    price = models.IntegerField()


class CafeItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to="cafe_item/", default="preview-page0.jpg")
    is_available = models.BooleanField()
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    sub_category = models.ForeignKey(
        "SubCategory",
        on_delete=models.PROTECT,
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

    def __str__(self) -> str:
        return self.name


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

    def __str__(self) -> str:
        return f"{self.review[:15]} ..."


class ParentCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="parent_category", default="preview-page0.jpg")

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="sub_category", default="preview-page0.jpg")
    parent_category_fk = models.ForeignKey(
        ParentCategory,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name
