# Generated by Django 5.1.7 on 2025-03-18 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0009_product_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
    ]
