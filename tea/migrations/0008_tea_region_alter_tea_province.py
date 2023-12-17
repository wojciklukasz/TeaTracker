# Generated by Django 5.0 on 2023-12-17 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0007_rename_country_region_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='tea',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.region'),
        ),
        migrations.AlterField(
            model_name='tea',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.province'),
        ),
    ]
