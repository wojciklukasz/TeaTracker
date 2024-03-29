# Generated by Django 4.2.8 on 2024-02-11 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0022_alter_store_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='province',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.country', verbose_name='Kraj'),
        ),
        migrations.AlterField(
            model_name='region',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.province', verbose_name='Prowincja'),
        ),
    ]
