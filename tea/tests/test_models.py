import os
from datetime import datetime

from django.test import TestCase
from django.utils.text import slugify

from tea.models import Country, Cultivar, Image, Profile, Province, Region, Tea, Type


class TeaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        profile = Profile.objects.create(name="default")
        tea_type = Type.objects.create(name="Zielona")
        cultivar = Cultivar.objects.create(name="Jiu Keng Quntizhong")
        country = Country.objects.create(name="Chiny")
        province = Province.objects.create(name="Zhejiang", country=country)
        region = Region.objects.create(name="Lin'an", province=province)

        tea_name = "Mingqian Long Jing 2023"
        Tea.objects.create(
            profile=profile,
            name=tea_name,
            slug=slugify(tea_name),
            price_per_100_grams=123,
            grams_left=100,
            country=country,
            province=province,
            region=region,
            type=tea_type,
            cultivar=cultivar,
            season="W",
            harvest_date=datetime(2023, 3, 25),
        )

    def setUp(self) -> None:
        session = self.client.session
        session["profile_id"] = Profile.objects.get(name="default").id
        session.save()

    def test_country_str(self):
        country = Country.objects.get(id=1)
        self.assertEqual(str(country), "Chiny")

    def test_tea_season(self):
        tea = Tea.objects.get(id=1)
        self.assertEqual(tea.season, "W")
        self.assertEqual(tea.get_season_display(), "Wiosna")

    def test_adding_images(self):
        image_path1 = os.path.join(os.getcwd(), "tea", "tests", "test_files", "1.jpg")
        image_path2 = os.path.join(os.getcwd(), "tea", "tests", "test_files", "2.jpg")
        tea = Tea.objects.get(id=1)
        Image.objects.create(image=image_path1, tea=tea)
        Image.objects.create(image=image_path2, tea=tea)

        self.assertEqual(len(Image.objects.filter(tea=tea).all()), 2)
