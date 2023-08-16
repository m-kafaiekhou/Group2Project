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
# class DynamicImages(models.Model):
#     logo = models.ImageField(upload_to="icons/", blank=True, null=True)
#     background = models.ImageField(upload_to="background/", blank=True, null=True)
#     gallery = models.ImageField(upload_to="gallery/", blank=True, null=True)


# class DynamicTexts(models.Model):
#     text = models.TextField()
#     email = models.EmailField()


# class DynamicNumbers(models.Model):
#     phone = PhoneField(null=True, blank=True, help_text="Phone numbers used on webpage")
#     cell_phone = PhoneNumberField(null=True, blank=True, unique=True)


class DynamicNumbers(models.Model):
    phone = PhoneField(null=True, blank=True, help_text="Phone numbers used on webpage")
    cell_phone = PhoneNumberField(null=True, blank=True, unique=True)


class Footer(models.Model):
    footer_name = models.CharField(max_length=25, default="main", unique=True)
    footer_is_active = models.BooleanField(default=True)

    contact_us_title = models.CharField(max_length=25, default="GET IN TOUCH")
    address = models.TextField(default="123 Street, New York, USA")
    phone_number = PhoneField(default="0211234567")
    email = models.EmailField(default="info@example.com")
    contact_us_is_active = models.BooleanField(default=True)

    follow_us_title = models.CharField(max_length=25, default="FOLLOW US")
    twitter_link = models.CharField(max_length=250, default="#")
    facebook_link = models.CharField(max_length=250, default="#")
    linkedin_link = models.CharField(max_length=250, default="#")
    instagram_link = models.CharField(max_length=250, default="#")
    follow_us_is_active = models.BooleanField(default=True)

    open_hours_title = models.CharField(max_length=25, default="OPEN HOURS")
    days1 = models.CharField(max_length=25, default="Monday- Friday")
    hours1 = models.CharField(max_length=25, default="8:00 AM- 10:00 PM")
    days2 = models.CharField(
        max_length=25, default="Saturday- Sunday", null=True, blank=True
    )
    hours2 = models.CharField(
        max_length=25, default="2:00 PM- 10:00 PM", null=True, blank=True
    )
    open_hours_is_active = models.BooleanField(default=True)

    newsletter_title = models.CharField(max_length=25, default="NEWSLETTER")
    newsletter_description = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        default="Enter your email to get the latest news",
    )
    newsletter_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.footer_name
