# Generated by Django 5.1.7 on 2025-03-19 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bought',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.FloatField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date_of_buying', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
