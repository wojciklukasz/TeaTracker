from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self) -> str:
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Cultivar(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'

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


class Tea(models.Model):
    SEASON_CHOICES = [('W', 'Wiosna'), ('L', 'Lato'), ('J', 'Jesien'), ('Z', 'Zima')]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    store = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL)

    price_per_100_grams = models.FloatField(validators=[MinValueValidator(1)])
    grams_left = models.IntegerField(validators=[MinValueValidator(0)])
    score = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    date_added = models.DateTimeField(auto_now_add=True)
    last_viewed = models.DateTimeField(default=timezone.now, blank=True)
    date_finished = models.DateField(null=True, blank=True)

    store_description = models.TextField(blank=True)
    user_description = models.TextField(blank=True)
    tasting_notes = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)

    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.SET_NULL
    )
    province = models.ForeignKey(
        Province, null=True, blank=True, on_delete=models.SET_NULL
    )
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.SET_NULL)

    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.SET_NULL)
    cultivar = models.ForeignKey(
        Cultivar, null=True, blank=True, on_delete=models.SET_NULL
    )

    season = models.CharField(blank=True, max_length=1, choices=SEASON_CHOICES)
    year = models.IntegerField(null=True, blank=True)
    harvest_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    tea = models.ForeignKey(Tea, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tea-images')

    def __str__(self) -> str:
        return f'{self.id} - {self.tea.name}'


class Brew(models.Model):
    tea = models.ForeignKey(Tea, on_delete=models.CASCADE)
    brew_date = models.DateField(auto_now_add=True)
    tasting_notes = models.TextField()

    def __str__(self) -> str:
        return f'{self.tea.name} {self.brew_date}'


class BrewImage(models.Model):
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='brew-images')

    def __str__(self) -> str:
        return f'{self.id} - {self.brew.brew_date} - {self.brew.tea}'
