from django.db import models
from menus.models import CafeItem
from django.core.validators import RegexValidator
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
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
    cafeitem = models.ForeignKey(
        CafeItem,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.review[:15]} ..."


# Coffee Shop Website DynamicInterface Models
class DynamicImages(models.Model):
    logo = models.ImageField(upload_to="icons/", blank=True, null=True)
    background = models.ImageField(upload_to="background/", blank=True, null=True)
    gallery = models.ImageField(upload_to="gallery/", blank=True, null=True)

class DynamicTexts(models.Model):
    text = models.TextField()
    email = models.EmailField()

