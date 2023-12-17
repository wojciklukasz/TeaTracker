from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Cultivar(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Brew(models.Model):
    brew_date = models.DateField(auto_now_add=True)
    tasting_notes = models.TextField()


class Store(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField()


class Profile(models.Model):
    name = models.CharField(max_length=50)


class Tea(models.Model):
    SEASON_CHOICES = {'Sp': 'Spring', 'Su': 'Summer', 'Au': 'Autumn', 'Wi': 'Winter'}

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    store = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)

    price_per_100_grams = models.FloatField(validators=[MinValueValidator(1)])
    grams_left = models.IntegerField(validators=[MinValueValidator(0)])
    score = models.IntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    date_added = models.DateField(auto_now_add=True)
    date_finished = models.DateField(null=True)

    store_description = models.TextField(blank=True)
    user_description = models.TextField(blank=True)
    tasting_notes = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    brews = models.ForeignKey(Brew, null=True, on_delete=models.SET_NULL)

    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    province = models.ForeignKey(Province, null=True, on_delete=models.SET_NULL)
    province = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)

    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)
    cultivar = models.ForeignKey(Cultivar, null=True, on_delete=models.SET_NULL)

    season = models.CharField(null=True, max_length=2, choices=SEASON_CHOICES)
    year = models.IntegerField(null=True)
    harvest_date = models.DateField(null=True)

    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    tea = models.ForeignKey(Tea, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tea-images')

    def __str__(self) -> str:
        return self.name
