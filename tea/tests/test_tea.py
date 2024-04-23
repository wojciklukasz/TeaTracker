from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from tea import models


class CreateTeaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        models.Profile.objects.create(name="create_tea")

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = models.Profile.objects.get(name="create_tea").id
        session.save()

        self.default_tea = {
            "name": "Test Tea",
            "price_per_100_grams": "1",
            "grams_left": "1",
            "profile_id": "1",
        }

    def test_page_load(self) -> None:
        response = self.client.get(reverse_lazy("create-tea"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h1>Nowa herbata</h1>", html=True)

    def test_incorrect_form(self) -> None:
        test_tea = self.default_tea.copy()
        test_tea["name"] = ""

        response = self.client.post(
            reverse_lazy("create-tea"),
            data=test_tea,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "To pole jest wymagane.")

    def test_valid_form(self) -> None:
        response = self.client.post(
            reverse_lazy("create-tea"),
            data=self.default_tea,
        )

        self.assertRedirects(
            response,
            reverse_lazy(
                "tea-detail", kwargs={"slug": models.Tea.objects.get(pk=1).slug}
            ),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

    def test_slug_creation(self) -> None:
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

    def test_unequal_dates(self) -> None:
        test_tea = self.default_tea.copy()
        test_tea["harvest_date"] = "2022-01-01"
        test_tea["year"] = "2023"

        response = self.client.post(
            reverse_lazy("create-tea"),
            data=test_tea,
        )

        self.assertContains(response, '<ul class="errorlist">')
        self.assertContains(response, "Rok nie zgadza się z datą zbiorów!")

    def test_future_dates(self) -> None:
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
        models.Profile.objects.create(name="create_others")

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = models.Profile.objects.get(name="create_others").id
        session.save()

    def test_plus_buttons(self) -> None:
        response = self.client.get(reverse_lazy("create-tea"))

        self.assertContains(
            response,
            'class="plus-href"',
            6,
        )

    def test_create_cultivar(self) -> None:
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

        response = self.client.post(
            reverse_lazy("create-tea"),
            data={
                "name": "Test",
                "slug": "test",
                "price_per_100_grams": "12",
                "grams_left": "12",
                "profile_id": "1",
                "cultivar": models.Cultivar.objects.get(pk=1).id,
            },
        )

        new_tea = models.Tea.objects.get(pk=1)

        self.assertRedirects(
            response,
            reverse_lazy("tea-detail", kwargs={"slug": new_tea.slug}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

        response = self.client.get(
            reverse_lazy("tea-detail", kwargs={"slug": new_tea.slug})
        )

        self.assertContains(response, cultivar_name)


class UpdateTeaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        profile = models.Profile.objects.create(name="update_tea")
        models.Tea.objects.create(
            name="Test Tea",
            slug="test-tea",
            price_per_100_grams=100,
            grams_left=100,
            profile=profile,
        )

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = models.Profile.objects.get(name="update_tea").id
        session.save()

        self.test_tea = models.Tea.objects.get(pk=1)

    def test_update_button(self) -> None:
        response = self.client.get(
            reverse_lazy(
                "tea-detail",
                kwargs={
                    "slug": self.test_tea.slug,
                },
            )
        )

        self.assertContains(response, 'id="update-button"')
        self.assertContains(response, f'href="/herbaty/{self.test_tea.slug}/edytuj"')

    def test_update_tea_grams(self) -> None:
        response = self.client.post(
            reverse_lazy("tea-update", kwargs={"slug": self.test_tea.slug}),
            data={
                "name": self.test_tea.name,
                "slug": self.test_tea.slug,
                "profile_id": self.test_tea.profile,
                "price_per_100_grams": self.test_tea.price_per_100_grams,
                "grams_left": 50,
            },
        )

        self.assertRedirects(
            response,
            reverse_lazy("tea-detail", kwargs={"slug": self.test_tea.slug}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

        response = self.client.get(
            reverse_lazy("tea-detail", kwargs={"slug": self.test_tea.slug})
        )

        self.assertContains(response, "50 g")
