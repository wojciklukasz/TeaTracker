# Generated by Django 5.0 on 2023-12-17 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0004_remove_tea_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='tea',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tea.tea'),
            preserve_default=False,
        ),
    ]