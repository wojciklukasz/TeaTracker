from http import HTTPStatus

from django.test import TestCase

from tea.models import Profile


class CreateTeaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Profile.objects.create(name='default')

    def test_page_load(self):
        response = self.client.get('/herbaty/nowa')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<h1>Nowa herbata</h1>', html=True)

    def test_incorrect_form(self):
        response = self.client.post(
            '/herbaty/nowa',
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
            '/herbaty/nowa',
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
            },
        )

        self.assertRedirects(
            response,
            '/herbaty/test-tea',
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

    def test_slug_creation(self):
        self.client.post(
            '/herbaty/nowa',
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
            },
        )

        response = self.client.post(
            '/herbaty/nowa',
            data={
                'name': 'Test Tea',
                'price_per_100_grams': '1',
                'grams_left': '1',
            },
        )

        self.assertRedirects(
            response,
            '/herbaty/test-tea-1',
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )
