from django.db import models
from django.db.models import Avg
from django.core.validators import RegexValidator
from staff.models import CustomUserModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Review(models.Model):
    class Rating(models.IntegerChoices):
        VERY_LOW = 1
        LOW = 2
        MIDDLE = 3
        HIGH = 4
        VERY_HIGH = 5

    rating = models.IntegerField(choices=Rating.choices, default=Rating.HIGH)

    review = models.CharField(max_length=300)
    cafeitem_fk = models.ForeignKey(
        CafeItem,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.review[:15]} ..."



