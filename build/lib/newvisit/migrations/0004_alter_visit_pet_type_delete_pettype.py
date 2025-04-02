# Generated by Django 5.1.7 on 2025-03-16 05:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newvisit', '0003_alter_visit_pet_type'),
        ('owners', '0002_alter_owner_pet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='pet_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owners.pettype'),
        ),
        migrations.DeleteModel(
            name='PetType',
        ),
    ]
