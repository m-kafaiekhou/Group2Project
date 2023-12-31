# Generated by Django 4.2.3 on 2023-08-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coffeeshop", "0002_alter_carouselitem_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="logo_image",
            field=models.ImageField(
                default="home_images/logo.png", upload_to="home_images"
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="logo_section_description",
            field=models.TextField(default="Our Beloved Logo"),
        ),
        migrations.AddField(
            model_name="homepage",
            name="logo_section_is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="homepage",
            name="logo_section_title",
            field=models.CharField(default="LOGO FUN", max_length=25),
        ),
    ]
