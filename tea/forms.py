from datetime import date
from typing import Any

from django import forms

from . import models


class TeaForm(forms.ModelForm):
    class Meta:
        model = models.Tea
        exclude = [
            'profile',
            'slug',
            'score',
            'date_added',
            'last_viewed',
            'date_finished',
        ]
        fields = [
            'name',
            'price_per_100_grams',
            'grams_left',
            'season',
            'year',
            'harvest_date',
            'store',
            'type',
            'cultivar',
            'country',
            'province',
            'region',
            'store_description',
            'user_description',
            'tasting_notes',
            'additional_notes',
        ]
        widgets = {
            'harvest_date': forms.DateInput(
                format='%d-%m-%Y',
                attrs={'type': 'date'},
            ),
        }

    def clean(self) -> dict[str, Any]:
        cleaned_data = super(TeaForm, self).clean()

        harvest_year = (
            cleaned_data.get('year') if cleaned_data.get('year') is not None else 1
        )
        if harvest_year > date.today().year:
            self.add_error('year', 'Rok produkcji jest większy niż aktualny rok!')

        harvest_date = (
            cleaned_data.get('harvest_date')
            if cleaned_data.get('harvest_date') is not None
            else date(1, 1, 1)
        )
        if harvest_date > date.today():
            self.add_error('harvest_date', 'Data zbiorów jest w przyszłości!')

        if harvest_year != harvest_date.year:
            self.add_error('year', 'Rok nie zgadza się z datą zbiorów!')

        return cleaned_data


class StoreForm(forms.ModelForm):
    class Meta:
        model = models.Store
        exclude = []


class TypeForm(forms.ModelForm):
    class Meta:
        model = models.Type
        exclude = []


class CultivarForm(forms.ModelForm):
    class Meta:
        model = models.Cultivar
        exclude = []


class CountryForm(forms.ModelForm):
    class Meta:
        model = models.Country
        exclude = []


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = models.Province
        exclude = []


class RegionForm(forms.ModelForm):
    class Meta:
        model = models.Region
        exclude = []
