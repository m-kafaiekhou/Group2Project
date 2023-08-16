from django.db import models
from menus.models import CafeItem
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

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

    date_added = models.DateTimeField(
        default=timezone.now,
        editable=False,
        blank=True,
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


class DynamicNumbers(models.Model):
    phone = PhoneField(null=True, blank=True, help_text="Phone numbers used on webpage")
    cell_phone = PhoneNumberField(null=True, blank=True, unique=True)


class DynamicNavbar(models.Model):
    pass


class DynamicFooter(models.Model):
    pass


class DynamicHomePage(models.Model):
    pass
