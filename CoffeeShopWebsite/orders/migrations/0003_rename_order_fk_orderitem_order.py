# Generated by Django 4.2.3 on 2023-08-07 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='order_fk',
            new_name='order',
        ),
    ]
