# Generated by Django 4.2.8 on 2023-12-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0013_brewimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brewimage',
            name='image',
            field=models.ImageField(upload_to='brew-images'),
        ),
    ]