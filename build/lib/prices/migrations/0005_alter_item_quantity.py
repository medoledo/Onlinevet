# Generated by Django 5.1.7 on 2025-03-19 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0004_alter_item_price_alter_item_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.FloatField(),
        ),
    ]
