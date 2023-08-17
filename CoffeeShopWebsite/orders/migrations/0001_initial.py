# Generated by Django 4.2.3 on 2023-08-16 04:09

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('C', 'Cancel'), ('A', 'Accept')], max_length=1)),
                ('phone_number', models.CharField(max_length=14, validators=[django.core.validators.RegexValidator('09(\\d{9})$', 'The phone number provided is invalid')], verbose_name='phone number')),
                ('order_date', models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 16, 4, 9, 35, 86875, tzinfo=datetime.timezone.utc), editable=False)),
                ('table_number', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('date_added', models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 16, 4, 9, 35, 87303, tzinfo=datetime.timezone.utc), editable=False)),
                ('cafeitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.cafeitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
