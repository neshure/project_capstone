# Generated by Django 4.1.4 on 2023-02-14 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smokeShop', '0009_orderitem_price_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='price_total',
        ),
    ]
