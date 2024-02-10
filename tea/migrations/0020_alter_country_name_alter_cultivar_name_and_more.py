# Generated by Django 4.2.8 on 2024-02-10 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0019_alter_tea_last_viewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='cultivar',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tea',
            name='season',
            field=models.CharField(blank=True, choices=[('W', 'Wiosna'), ('L', 'Lato'), ('J', 'Jesień'), ('Z', 'Zima')], max_length=1),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
