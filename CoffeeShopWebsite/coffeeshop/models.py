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


# Creat Dynamic Models


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


class HomePage(models.Model):
    homepage_name = models.CharField(max_length=25, default="main", unique=True)
    webpage_title = models.CharField(max_length=25, default="TEHRAN Coffee Shop")

    search_section_is_active = models.BooleanField(default=True)
    search_section_title = models.CharField(max_length=25, default="SEARCH")
    search_section_description = models.TextField(default="Search for Drinks")
    search_placeholder = models.CharField(max_length=100, default="Search Here")

    logo_section_is_active = models.BooleanField(default=True)
    logo_section_title = models.CharField(max_length=25, default="LOGO FUN")
    logo_section_description = models.TextField(default="Our Beloved Logo")
    logo_image = models.ImageField(
        upload_to="home_images", default="home_images/logo.png"
    )
    about_us_section_is_active = models.BooleanField(default=True)
    about_us_section_title = models.CharField(max_length=25, default="ABOUT US")
    about_us_section_description = models.TextField(default="Serving Since 2023")
    about_us_image = models.ImageField(
        upload_to="home_images", default="home_images/about.png"
    )
    left_about_us_title = models.CharField(max_length=25, default="Our Story")
    left_about_us_description = models.TextField(null=True, blank=True)
    left_about_us_button_text = models.CharField(max_length=25, default="Learn More")
    right_about_us_title = models.CharField(max_length=25, default="Our Vision")
    right_about_us_description = models.TextField(null=True, blank=True)
    right_about_us_first_option = models.CharField(
        max_length=50, default="Lorem ipsum dolor sit amet"
    )
    right_about_us_second_option = models.CharField(
        max_length=50, default="Lorem ipsum dolor sit amet"
    )
    right_about_us_third_option = models.CharField(
        max_length=50, default="Lorem ipsum dolor sit amet"
    )
    right_about_us_button_text = models.CharField(max_length=25, default="Learn More")

    our_services_section_is_active = models.BooleanField(default=True)
    our_services_section_title = models.CharField(max_length=25, default="OUR SERVICES")
    our_services_section_description = models.TextField(default="Fresh & Organic Beans")

    offer_section_is_active = models.BooleanField(default=True)
    offer_section_title = models.CharField(max_length=25, default="50% OFF")
    offer_section_short_description = models.TextField(default="Sunday Special Offer")
    offer_section_long_description = models.TextField(
        default="Only for Sunday from 1st Jan to 30th Jan 2045"
    )

    menu_special_items_section_is_active = models.BooleanField(default=True)
    menu_special_items_section_title = models.CharField(
        max_length=25, default="TOP RATED ITEMS"
    )
    menu_special_items_section_description = models.TextField(
        default="The Best Items According to Our Customers"
    )

    testimonial_section_is_active = models.BooleanField(default=True)
    testimonial_section_title = models.CharField(max_length=25, default="TESTIMONIAL")
    testimonial_section_description = models.TextField(default="Our Clients Say")

    def __str__(self):
        return self.homepage_name


class CarouselItem(models.Model):
    image = models.ImageField(
        upload_to="home_images", default="home_images/carousel-1.jpg"
    )
    first_line_text = models.TextField(default="We Have Been Serving")
    second_line_text = models.CharField(max_length=25, default="COFFEE")
    third_line_text = models.TextField(default="* SINCE 2023 *")
    page = models.ForeignKey(
        HomePage,
        on_delete=models.SET_NULL,
        null=True,
        related_name="carousel_items",
    )


class Service(models.Model):
    image = models.ImageField(upload_to="home_images", default="#")
    icon_class = models.CharField(max_length=50, null=True, blank=True)
    service_title = models.CharField(max_length=100)
    service_description = models.TextField
    page = models.ForeignKey(
        HomePage,
        on_delete=models.SET_NULL,
        null=True,
        related_name="services_list",
    )
