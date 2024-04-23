from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from tea import models


class CreateTeaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        models.Profile.objects.create(name="default")

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = models.Profile.objects.get(name="default").id
        session.save()

        self.default_tea = {
            "name": "Test Tea",
            "price_per_100_grams": "1",
            "grams_left": "1",
        }

    def test_page_load(self):
        response = self.client.get(reverse_lazy("create-tea"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Nowa herbata</h1>", html=True)

    def test_incorrect_form(self):
        test_tea = self.default_tea.copy()
        test_tea["name"] = ""

        response = self.client.post(
            reverse_lazy("create-tea"),
            data=test_tea,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "To pole jest wymagane.")

    def test_valid_form(self):
        response = self.client.post(
            reverse_lazy("create-tea"),
            data=self.default_tea,
        )

        self.assertRedirects(
            response,
            reverse_lazy("tea-detail", kwargs={"slug": "test-tea"}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

    def test_slug_creation(self):
        self.client.post(
            reverse_lazy("create-tea"),
            data=self.default_tea,
        )

        response = self.client.post(
            reverse_lazy("create-tea"),
            data=self.default_tea,
        )

        self.assertRedirects(
            response,
            reverse_lazy("tea-detail", kwargs={"slug": "test-tea-1"}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

    def test_unequal_dates(self):
        test_tea = self.default_tea.copy()
        test_tea["harvest_date"] = "2022-01-01"
        test_tea["year"] = "2023"

        response = self.client.post(
            reverse_lazy("create-tea"),
            data=test_tea,
        )

        self.assertContains(response, '<ul class="errorlist">')
        self.assertContains(response, "Rok nie zgadza się z datą zbiorów!")

    def test_future_dates(self):
        test_tea = self.default_tea.copy()
        test_tea["harvest_date"] = "2025-01-01"
        test_tea["year"] = "2025"

        response = self.client.post(
            reverse_lazy("create-tea"),
            data=test_tea,
        )

        self.assertContains(response, '<ul class="errorlist">')
        self.assertContains(response, "Rok produkcji jest większy niż aktualny rok!")
        self.assertContains(response, "Data zbiorów jest w przyszłości!")


class CreateOthersTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        models.Profile.objects.create(name="default")

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = models.Profile.objects.get(name="default").id
        session.save()

    def test_plus_buttons(self):
        response = self.client.get(reverse_lazy("create-tea"))

        self.assertContains(
            response,
            'class="plus-href"',
            6,
        )

    def test_create_cultivar(self):
        cultivar_name = "Test Cultivar"

        response = self.client.post(
            reverse_lazy("create-cultivar"),
            data={
                "name": cultivar_name,
            },
        )

        self.assertRedirects(
            response,
            reverse_lazy("create-tea"),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

        test_tea = self.default_tea.copy()
        test_tea["cultivar"] = models.Cultivar.objects.get(name=cultivar_name).id

        response = self.client.post(
            reverse_lazy("create-tea"),
            data=test_tea,
        )

        self.assertRedirects(
            response,
            reverse_lazy("tea-detail", kwargs={"slug": "test-tea"}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

        response = self.client.get(
            reverse_lazy("tea-detail", kwargs={"slug": "test-tea"})
        )

        self.assertContains(response, cultivar_name)
