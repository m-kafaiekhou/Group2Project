from django.db import models
from django.core.validators import RegexValidator
from staff.models import CustomUserModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


def regex_validation():
    _REGEX = r"09(\d{9})$"
    phone_validator = RegexValidator(_REGEX, "The phone number provided is invalid")
    return phone_validator


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
    order_date = models.DateTimeField(auto_now_add=True)  # core app
    table_number = models.IntegerField(default=None)
    staff = models.ForeignKey(
        CustomUserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.phone_number

    def get_order_items(self):
        return self.orderitem_set.all()

    def get_total_price(self):
        items = self.get_order_items()
        total = 0
        for item in items:
            total += item.price

        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    cafeitem = models.ForeignKey(
        "menus.CafeItem",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()
    price = models.IntegerField()

    def set_price(self):
        self.price = self.cafeitem.price * self.quantity

    def save(self, *args, **kwargs):
        self.set_price()
        super().save(*args, **kwargs)
