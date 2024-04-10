from django.test import TestCase
from django.urls import reverse_lazy

from tea.models import Profile


class ProfilesTestCase(TestCase):
    test_profile_name = "test_profile"

    def initial_load_test(self) -> None:
        response = self.client.get("")
        self.assertRedirects(response, "/profil")
        self.assertContains(response, "Aktualnie nie wybrano żadnego profilu!")

    def test_profile_selection(self) -> None:
        profile = Profile.objects.create(name=self.test_profile_name)

        self.client.post(
            reverse_lazy("profile-select"),
            data={"profile": profile.id},
        )

        response = self.client.get(reverse_lazy("profile-select"))
        self.assertContains(response, f"Aktualny profil: {self.test_profile_name}")

    def test_profile_creation(self) -> None:
        self.client.post(
            reverse_lazy("create-profile"),
            data={"name": self.test_profile_name},
        )
        self.assertEqual(Profile.objects.get(name=self.test_profile_name).id, 1)

        response = self.client.get(reverse_lazy("profile-select"))
        self.assertContains(
            response, f'<option value="1">{self.test_profile_name}</option>', html=True
        )

    def test_duplicate_profiles(self) -> None:
        self.client.post(
            reverse_lazy("create-profile"),
            data={"name": self.test_profile_name},
        )
        response = self.client.post(
            reverse_lazy("create-profile"),
            data={"name": self.test_profile_name},
        )

        self.assertContains(response, "Istnieje już Profil z tą wartością pola Nazwa.")

    def test_profile_selection_view(self) -> None:
        response = self.client.get(reverse_lazy("profile-select"))
        self.assertContains(response, "Aktualnie nie wybrano żadnego profilu!")
        self.assertContains(
            response,
            f'href="{reverse_lazy("create-profile")}"',
        )
