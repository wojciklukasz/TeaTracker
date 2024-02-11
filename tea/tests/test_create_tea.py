from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from tea import models


class CreateTeaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        models.Profile.objects.create(name='default')

    def test_page_load(self):
        response = self.client.get(reverse_lazy('create-tea'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<h1>Nowa herbata</h1>', html=True)

    def test_incorrect_form(self):
        response = self.client.post(
            reverse_lazy('create-tea'),
            data={
                'name': '',
                'price_per_100_grams': '1',
                'grams_left': '1',
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'To pole jest wymagane.')

    def test_valid_form(self):
        response = self.client.post(
            reverse_lazy('create-tea'),
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
            },
        )

        self.assertRedirects(
            response,
            reverse_lazy('tea-detail', kwargs={'slug': 'test-tea'}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

    def test_slug_creation(self):
        self.client.post(
            reverse_lazy('create-tea'),
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
            },
        )

        response = self.client.post(
            reverse_lazy('create-tea'),
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
            },
        )

        self.assertRedirects(
            response,
            reverse_lazy('tea-detail', kwargs={'slug': 'test-tea-1'}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

    def test_unequal_dates(self):
        response = self.client.post(
            reverse_lazy('create-tea'),
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
                'harvest_date': '2022-01-01',
                'year': '2023',
            },
        )

        # print(response.content)
        # self.assertContains(response, '<ul class="errorlist">', html=True)
        self.assertContains(response, 'Rok nie zgadza się z datą zbiorów!')

    def test_future_dates(self):
        response = self.client.post(
            reverse_lazy('create-tea'),
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
                'harvest_date': '2025-01-01',
                'year': '2025',
            },
        )

        # print(response.content)
        # self.assertContains(response, '<ul class="errorlist">', html=True)
        self.assertContains(response, 'Rok produkcji jest większy niż aktualny rok!')
        self.assertContains(response, 'Data zbiorów jest w przyszłości!')

    def test_plus_buttons(self):
        response = self.client.get(reverse_lazy('create-tea'))

        self.assertContains(
            response,
            'class="plus-href"',
            6,
        )

    def test_create_cultivar(self):
        response = self.client.post(
            reverse_lazy('create-cultivar'),
            data={
                'name': 'Test Cultivar',
            },
        )

        self.assertRedirects(
            response,
            reverse_lazy('create-tea'),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

        response = self.client.post(
            reverse_lazy('create-tea'),
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
                'cultivar': models.Cultivar.objects.get(name='Test Cultivar').id,
            },
        )

        self.assertRedirects(
            response,
            reverse_lazy('tea-detail', kwargs={'slug': 'test-tea'}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

        response = self.client.get(
            reverse_lazy('tea-detail', kwargs={'slug': 'test-tea'})
        )

        self.assertContains(response, 'Test Cultivar')
