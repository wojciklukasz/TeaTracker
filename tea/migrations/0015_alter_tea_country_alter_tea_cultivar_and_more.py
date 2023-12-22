# Generated by Django 4.2.8 on 2023-12-22 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0014_alter_brewimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tea',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.country'),
        ),
        migrations.AlterField(
            model_name='tea',
            name='cultivar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.cultivar'),
        ),
        migrations.AlterField(
            model_name='tea',
            name='harvest_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tea',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.province'),
        ),
        migrations.AlterField(
            model_name='tea',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.region'),
        ),
        migrations.AlterField(
            model_name='tea',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.store'),
        ),
        migrations.AlterField(
            model_name='tea',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.type'),
        ),
        migrations.AlterField(
            model_name='tea',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]