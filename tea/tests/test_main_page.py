import os

from django.test import TestCase
from django.utils.text import slugify

from tea.models import Image, Profile, Tea


class MainPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        profile = Profile.objects.create(name="default")

        tea_names = ["One", "Two", "Three"]
        for tea_name in tea_names:
            tea = Tea.objects.create(
                profile=profile,
                name=tea_name,
                slug=slugify(tea_name),
                price_per_100_grams=123,
                grams_left=100,
            )
        image_path = os.path.join(os.getcwd(), "tea", "tests", "test_files", "1.jpg")
        Image.objects.create(tea=tea, image=image_path)

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = Profile.objects.get(name="default").id
        session.save()

    def test_page_load(self) -> None:
        response = self.client.get("")
        self.assertContains(response, "Ostatnio dodane herbaty")

    def test_item_lists(self) -> None:
        response = self.client.get("")
        self.assertContains(response, "</ul>", count=3, html=False)
        self.assertContains(response, "</li>", count=9, html=False)

    def test_images(self) -> None:
        response = self.client.get("")
        self.assertContains(response, "1.jpg", count=3, html=False)
