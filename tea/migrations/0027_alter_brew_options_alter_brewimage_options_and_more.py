# Generated by Django 4.2.8 on 2024-04-10 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tea', '0026_alter_profile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brew',
            options={'verbose_name': 'Parzenie', 'verbose_name_plural': 'Parzenia'},
        ),
        migrations.AlterModelOptions(
            name='brewimage',
            options={'verbose_name': 'Zdjęcie parzenia', 'verbose_name_plural': 'Zdjęcia parzeń'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Kraj', 'verbose_name_plural': 'Kraje'},
        ),
        migrations.AlterModelOptions(
            name='cultivar',
            options={'verbose_name': 'Kultywar', 'verbose_name_plural': 'Kultywary'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Zdjęcie', 'verbose_name_plural': 'Zdjęcia'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profil', 'verbose_name_plural': 'Profile'},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'verbose_name': 'Prowincja', 'verbose_name_plural': 'Prowincje'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Region', 'verbose_name_plural': 'Regiony'},
        ),
        migrations.AlterModelOptions(
            name='store',
            options={'verbose_name': 'Sklep', 'verbose_name_plural': 'Sklepy'},
        ),
        migrations.AlterModelOptions(
            name='tea',
            options={'verbose_name': 'Herbata', 'verbose_name_plural': 'Herbaty'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': 'Typ herbaty', 'verbose_name_plural': 'Typy herbaty'},
        ),
    ]