from model_mommy import mommy

from django.shortcuts import resolve_url
from django.test import TestCase

from cities.models import City
from meupet.models import Kind, Pet, PetStatus
from users.models import OwnerProfile


class ListPetsTest(TestCase):
    def setUp(self):
        mommy.make(City, name="Araras", search_name="araras")

        OwnerProfile.objects.create_user(
            "johndoe",
            "john@example.com",
            "secret",
            first_name="John",
            last_name="Doe",
            facebook="https://fb.com/4",
        )

        self.pet_status = mommy.make(PetStatus)

        self.pet = Pet.objects.create(
            owner=OwnerProfile.objects.first(),
            name="Dorinha",
            description="Doralice",
            city=City.objects.first(),
            kind=Kind.objects.first(),
            status=self.pet_status,
            size=Pet.SMALL,
            sex=Pet.FEMALE,
            published=True,
        )

        self.resp = self.client.get(resolve_url("api:list_pets"))

    def test_status(self):
        """Should return 200 as status code"""
        self.assertEqual(200, self.resp.status_code)

    def test_content_type(self):
        """Content-Type should be json"""
        self.assertEqual("application/json", self.resp["Content-Type"])

    def test_content(self):
        """Should return the most important data, like name, description and city"""
        result = self.resp.content.decode()
        pet_profile = resolve_url("meupet:detail", self.pet.slug)
        user_profile = resolve_url("users:user_profile", self.pet.owner.id)

        contents = (
            "Araras",
            "Doralice",
            "Gato",
            "Dorinha",
            "Female",
            self.pet_status.description,
            "Small",
            pet_profile,
            user_profile,
            "https://fb.com/4",
        )

        for expected in contents:
            with self.subTest():
                self.assertIn(expected, result)
