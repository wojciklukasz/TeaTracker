# Generated by Django 4.2.11 on 2024-04-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0028_brew_grams_brew_water_ml'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brew',
            name='tasting_notes',
            field=models.TextField(verbose_name='Opis'),
        ),
    ]
