# Generated by Django 4.1.4 on 2023-02-07 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smokeShop', '0003_remove_cart_product_remove_cart_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='label',
        ),
    ]
