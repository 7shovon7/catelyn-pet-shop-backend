# Generated by Django 5.0.6 on 2024-09-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_product_available_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='custom_stock_out_signal',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
