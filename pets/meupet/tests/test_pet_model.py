from django.test import TestCase

from meupet.models import Pet, City
from users.models import OwnerProfile


class PetTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(city='Testing City')
        self.owner = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.pet = Pet.objects.create(name='Lost Pet', city=self.city, owner=self.owner)

    def test_slug(self):
        self.assertEqual('lost-pet-testing-city', self.pet.slug)

    def test_slug_uniqueness(self):
        pet_2 = Pet.objects.create(name='Lost Pet', city=self.city, owner=self.owner)
        pet_3 = Pet.objects.create(name='Lost Pet', city=self.city, owner=self.owner)

        self.assertEqual('lost-pet-testing-city-2', pet_2.slug)
        self.assertEqual('lost-pet-testing-city-3', pet_3.slug)
