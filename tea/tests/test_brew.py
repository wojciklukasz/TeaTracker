from datetime import date
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from tea import models


class CreateBrewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        profile = models.Profile.objects.create(name="default")
        models.Tea.objects.create(
            name="Test tea",
            slug="test_tea",
            price_per_100_grams=1,
            grams_left=1,
            profile=profile,
        )

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = models.Profile.objects.get(name="default").id
        session.save()

        self.test_tea = models.Tea.objects.get(slug="test_tea")
        self.default_brew = {
            "tea": self.test_tea,
            "tasting_notes": "Tasty test",
            "grams": 5,
            "water_ml": 100,
        }

        # used for comparing dates, which use polish month names
        self.months_translated = {
            1: "stycznia",
            2: "lutego",
            3: "marca",
            4: "kwietnia",
            5: "maja",
            6: "czerwca",
            7: "lipca",
            8: "sierpnia",
            9: "września",
            10: "października",
            11: "listopada",
            12: "grudnia",
        }

    def test_button(self) -> None:
        response = self.client.get(
            reverse_lazy(
                "tea-detail",
                kwargs={
                    "slug": self.test_tea.slug,
                },
            )
        )

        self.assertContains(response, 'id="brews-list-button"')
        self.assertContains(response, 'href="/herbaty/test_tea/parzenia/"')

    def test_create_brew(self) -> None:
        response = self.client.post(
            reverse_lazy(
                "create-brew",
                kwargs={"slug": self.test_tea.slug},
            ),
            data=self.default_brew,
        )

        self.assertRedirects(
            response,
            reverse_lazy("tea-detail", kwargs={"slug": self.test_tea.slug}),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
        )

        response = self.client.get(
            reverse_lazy(
                "brews-list",
                kwargs={
                    "slug": self.test_tea.slug,
                },
            )
        )

        cur_date = date.today()
        self.assertContains(
            response,
            f"{cur_date.day} {self.months_translated[cur_date.month]} {cur_date.year}",
        )

        ratio = str(models.Brew.objects.get(pk=1).ratio).replace(
            ".", ","
        )  # polish locale uses , for decimals
        self.assertContains(response, ratio)

    def test_brew_details(self) -> None:
        self.client.post(
            reverse_lazy(
                "create-brew",
                kwargs={"slug": self.test_tea.slug},
            ),
            data=self.default_brew,
        )

        brew = models.Brew.objects.get(pk=1)

        response = self.client.get(
            reverse_lazy(
                "brew-detail",
                kwargs={"pk": brew.pk},
            )
        )

        self.assertContains(response, str(brew.grams).replace(".", ","))
        self.assertContains(response, brew.water_ml)
        self.assertContains(response, brew.tasting_notes)
