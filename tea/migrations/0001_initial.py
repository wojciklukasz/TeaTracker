# Generated by Django 5.0 on 2023-12-17 15:15

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brew_date', models.DateField(auto_now_add=True)),
                ('tasting_notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Cultivar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tea-images')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.country')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.province')),
            ],
        ),
        migrations.CreateModel(
            name='Tea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('price_per_100_grams', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('grams_left', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('score', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_finished', models.DateField(null=True)),
                ('store_description', models.TextField(blank=True)),
                ('user_description', models.TextField(blank=True)),
                ('tasting_notes', models.TextField(blank=True)),
                ('additional_notes', models.TextField(blank=True)),
                ('season', models.CharField(choices=[('Sp', 'Spring'), ('Su', 'Summer'), ('Au', 'Autumn'), ('Wi', 'Winter')], max_length=2, null=True)),
                ('year', models.IntegerField(null=True)),
                ('harvest_date', models.DateField(null=True)),
                ('brews', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.brew')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.country')),
                ('cultivar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.cultivar')),
                ('images', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.images')),
                ('province', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.region')),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.store')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tea.type')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('teas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tea.tea')),
            ],
        ),
    ]
