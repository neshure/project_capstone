# Generated by Django 4.1.4 on 2023-02-10 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smokeShop', '0005_remove_orderitem_item_orderitem_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
