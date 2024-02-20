from __future__ import annotations

from datetime import date
from typing import Any, Dict

from django import forms

from . import models


class ProfileSelectForm(forms.ModelForm):
    class Meta:
        model = models.Tea
        fields = ['profile']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['name']


class TeaForm(forms.ModelForm):
    class Meta:
        model = models.Tea
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

    def clean(self) -> Dict[str, Any]:
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
        fields = ['name', 'website']


class TypeForm(forms.ModelForm):
    class Meta:
        model = models.Type
        fields = ['name']


class CultivarForm(forms.ModelForm):
    class Meta:
        model = models.Cultivar
        fields = ['name']


class CountryForm(forms.ModelForm):
    class Meta:
        model = models.Country
        fields = ['name']


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = models.Province
        fields = ['name', 'country']


class RegionForm(forms.ModelForm):
    class Meta:
        model = models.Region
        fields = ['name', 'province']
