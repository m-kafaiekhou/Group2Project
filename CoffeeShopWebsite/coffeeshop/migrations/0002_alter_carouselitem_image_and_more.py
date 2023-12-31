# Generated by Django 4.2.3 on 2023-08-17 00:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coffeeshop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carouselitem",
            name="image",
            field=models.ImageField(
                default="home_images/carousel-1.jpg", upload_to="home_images"
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="about_us_image",
            field=models.ImageField(
                default="home_images/about.png", upload_to="home_images"
            ),
        ),
    ]
