# Generated by Django 4.1.4 on 2023-02-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smokeShop', '0007_alter_order_ordered_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user_review',
            field=models.TextField(blank=True, null=True),
        ),
    ]
