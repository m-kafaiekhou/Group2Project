# Generated by Django 4.2.3 on 2023-08-29 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coffeeshop", "0005_navbar"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dashboard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dashboard_name",
                    models.CharField(default="main", max_length=25, unique=True),
                ),
                ("short_name", models.CharField(default="G2", max_length=10)),
                ("cafe_name", models.CharField(default="TEHRAN", max_length=50)),
            ],
        ),
    ]