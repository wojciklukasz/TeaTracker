from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Cultivar(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country)

    def __str__(self) -> str:
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Province)

    def __str__(self) -> str:
        return self.name


class Brew(models.Model):
    brew_date = models.DateField(auto_now_add=True)
    tasting_notes = models.CharField()


class Store(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField()


class Images(models.Model):
    image = models.ImageField(upload_to='tea-images')


class Tea(models.Model):
    SEASON_CHOICES = {'Sp': 'Spring', 'Su': 'Summer', 'Au': 'Autumn', 'Wi': 'Winter'}

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    store = models.ForeignKey(Store, null=True)
    images = models.ForeignKey(Images, null=True)

    price_per_100_grams = models.FloatField(validate=[MinValueValidator(1)])
    grams_left = models.IntegerField(validate=[MinValueValidator(0)])
    score = models.IntegerField(
        null=True, validate=[MinValueValidator(1), MaxValueValidator(10)]
    )

    date_added = models.DateField(auto_now_add=True)
    date_finished = models.DateField(null=True)

    store_description = models.TextField(blank=True)
    user_description = models.TextField(blank=True)
    tasting_notes = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    brews = models.ForeignKey(Brew, null=True)

    country = models.ForeignKey(Country, null=True)
    province = models.ForeignKey(Province, null=True)
    province = models.ForeignKey(Region, null=True)

    type = models.ForeignKey(Type)
    cultivar = models.ForeignKey(Cultivar, null=True)

    season = models.CharField(null=True, max_length=2, choices=SEASON_CHOICES)
    year = models.IntegerField(null=True)
    harvest_date = models.DateField(null=True)

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=50)
    teas = models.ForeignKey(Tea, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
