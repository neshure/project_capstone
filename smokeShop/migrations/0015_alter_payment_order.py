# Generated by Django 4.1.4 on 2023-02-17 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smokeShop', '0014_rename_created_payment_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='smokeShop.order'),
        ),
    ]
