# Generated by Django 4.2.8 on 2023-12-22 17:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0018_alter_tea_last_viewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tea',
            name='last_viewed',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
