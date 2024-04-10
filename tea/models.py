from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Nazwa"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Profil")
        verbose_name_plural = _("Profile")


class Store(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Nazwa"))
    website = models.URLField(unique=True, verbose_name=_("Strona internetowa"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Sklep")
        verbose_name_plural = _("Sklepy")


class Type(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name=_("Nazwa"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Typ herbaty")
        verbose_name_plural = _("Typy herbaty")


class Cultivar(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Nazwa"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Kultywar")
        verbose_name_plural = _("Kultywary")


class Country(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name=_("Nazwa"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Kraj")
        verbose_name_plural = _("Kraje")


class Province(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_("Nazwa"))
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_("Kraj")
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Prowincja")
        verbose_name_plural = _("Prowincje")


class Region(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_("Nazwa"))
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name=_("Prowincja")
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regiony")


class Tea(models.Model):
    SEASON_CHOICES = [("W", "Wiosna"), ("L", "Lato"), ("J", "Jesień"), ("Z", "Zima")]

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name=_("Profil")
    )
    name = models.CharField(max_length=100, verbose_name=_("Nazwa"))
    slug = models.SlugField(unique=True)
    store = models.ForeignKey(
        Store, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("Sklep")
    )

    price_per_100_grams = models.FloatField(
        validators=[MinValueValidator(1)], verbose_name=_("Cena za 100 gramów")
    )
    grams_left = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name=_("Pozostało gramów")
    )
    score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_("Ocena"),
    )

    date_added = models.DateTimeField(auto_now_add=True)
    last_viewed = models.DateTimeField(default=timezone.now, blank=True)
    date_finished = models.DateField(null=True, blank=True)

    store_description = models.TextField(blank=True, verbose_name=_("Opis sprzedawcy"))
    user_description = models.TextField(blank=True, verbose_name=_("Opis własny"))
    tasting_notes = models.TextField(blank=True, verbose_name=_("Nuty smakowe"))
    additional_notes = models.TextField(blank=True, verbose_name=_("Dodatkowe uwagi"))

    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Kraj"),
    )
    province = models.ForeignKey(
        Province,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Prowincja"),
    )
    region = models.ForeignKey(
        Region,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Region"),
    )

    type = models.ForeignKey(
        Type,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Typ herbaty"),
    )
    cultivar = models.ForeignKey(
        Cultivar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Kultywar"),
    )

    season = models.CharField(
        blank=True, max_length=1, choices=SEASON_CHOICES, verbose_name=_("Sezon")
    )
    year = models.IntegerField(null=True, blank=True, verbose_name=_("Rok"))
    harvest_date = models.DateField(
        null=True, blank=True, verbose_name=_("Data zbiorów")
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Herbata")
        verbose_name_plural = _("Herbaty")


class Image(models.Model):
    tea = models.ForeignKey(Tea, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tea-images")

    def __str__(self) -> str:
        return f"{self.id} - {self.tea.name}"

    class Meta:
        verbose_name = _("Zdjęcie")
        verbose_name_plural = _("Zdjęcia")


class Brew(models.Model):
    tea = models.ForeignKey(Tea, on_delete=models.CASCADE)
    brew_date = models.DateField(auto_now_add=True)
    tasting_notes = models.TextField()

    def __str__(self) -> str:
        return f"{self.tea.name} {self.brew_date}"

    class Meta:
        verbose_name = _("Parzenie")
        verbose_name_plural = _("Parzenia")


class BrewImage(models.Model):
    brew = models.ForeignKey(Brew, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="brew-images")

    def __str__(self) -> str:
        return f"{self.id} - {self.brew.brew_date} - {self.brew.tea}"

    class Meta:
        verbose_name = _("Zdjęcie parzenia")
        verbose_name_plural = _("Zdjęcia parzeń")
