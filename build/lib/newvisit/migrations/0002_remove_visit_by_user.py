# Generated by Django 5.1.7 on 2025-03-16 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newvisit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='by_user',
        ),
    ]
