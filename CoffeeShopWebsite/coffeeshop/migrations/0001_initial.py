# Generated by Django 4.2.3 on 2023-08-16 04:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='icons/')),
                ('background', models.ImageField(blank=True, null=True, upload_to='background/')),
                ('gallery', models.ImageField(blank=True, null=True, upload_to='gallery/')),
            ],
        ),
        migrations.CreateModel(
            name='DynamicNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Phone numbers used on webpage', max_length=31, null=True)),
                ('cell_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DynamicTexts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Middle'), (4, 'High'), (5, 'Very High')], default=4)),
                ('review', models.CharField(max_length=300)),
                ('date_added', models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 16, 4, 9, 35, 84253, tzinfo=datetime.timezone.utc), editable=False)),
                ('cafeitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.cafeitem')),
            ],
        ),
    ]
