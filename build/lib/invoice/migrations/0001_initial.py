# Generated by Django 5.1.7 on 2025-03-16 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.IntegerField(default=1)),
                ('discount', models.IntegerField(default=0)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('exp', models.DateField()),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prices.item')),
            ],
        ),
    ]
