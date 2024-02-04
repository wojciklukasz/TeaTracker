from datetime import date
from typing import Any

from django import forms

from .models import Tea


class TeaForm(forms.ModelForm):
    class Meta:
        model = Tea
        exclude = [
            'profile',
            'slug',
            'score',
            'date_added',
            'last_viewed',
            'date_finished',
        ]
        labels = {
            'name': 'Nazwa',
            'store': 'Sklep',
            'price_per_100_grams': 'Cena za 100 gramów',
            'grams_left': 'Pozostało gramów',
            'store_description': 'Opis sprzedawcy',
            'user_description': 'Opis użytkownika',
            'tasting_notes': 'Nuty smakowe',
            'additional_notes': 'Dodatkowe uwagi',
            'country': 'Kraj',
            'province': 'Prowincja',
            'region': 'Region',
            'type': 'Typ herbaty',
            'cultivar': 'Kultywar',
            'season': 'Sezon',
            'year': 'Rok',
            'harvest_date': 'Data zbiorów',
        }
        fields = [
            'name',
            'price_per_100_grams',
            'grams_left',
            'store',
            'country',
            'province',
            'region',
            'type',
            'cultivar',
            'season',
            'year',
            'harvest_date',
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

        print(cleaned_data)

        harvest_year = (
            cleaned_data.get('year') if cleaned_data.get('year') is not None else 0
        )
        if harvest_year > date.today().year:
            self.add_error('year', 'Rok produkcji jest większy niż aktualny rok!')

        return cleaned_data
