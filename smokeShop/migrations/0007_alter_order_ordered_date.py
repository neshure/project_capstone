# Generated by Django 4.1.4 on 2023-02-10 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smokeShop', '0006_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
