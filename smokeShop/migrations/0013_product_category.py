# Generated by Django 4.1.4 on 2023-02-15 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smokeShop', '0012_alter_orderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
