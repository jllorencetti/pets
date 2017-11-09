from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from cities.models import City
from meupet.models import Pet
from users.models import OwnerProfile


class PetModelTest(TestCase):
    def setUp(self):
        self.city = mommy.make(City, name='Testing City')
        self.owner = OwnerProfile.objects.create_user(username='admin', password='admin')

    def test_slug(self):
        """Slug should contains both the pet name and city"""
        pet = mommy.make(Pet, name='Lost Pet', city=self.city, slug=None)
        self.assertEqual('lost-pet-testing-city', pet.slug)

    def test_slug_uniqueness(self):
        """Should auto append a number if the slug is not unique"""
        pet = mommy.make(Pet, name='Lost Pet', city=self.city, slug=None)
        pet_two = mommy.make(Pet, name='Lost Pet', city=self.city, slug=None)

        self.assertEqual('lost-pet-testing-city', pet.slug)
        self.assertEqual('lost-pet-testing-city-2', pet_two.slug)

    def test_staled_pets(self):
        """Should return only pets that are staled and are still lost or for adoption"""
        new_missing_pet = mommy.make(Pet, status=Pet.MISSING)
        new_adoption_pet = mommy.make(Pet, status=Pet.FOR_ADOPTION)
        staled_missing_pet = self.create_pet_custom_date(90, status=Pet.MISSING)
        staled_adoption_pet = self.create_pet_custom_date(90, status=Pet.FOR_ADOPTION)
        staled_found_pet = self.create_pet_custom_date(90, status=Pet.FOUND)
        staled_adopted_pet = self.create_pet_custom_date(90, status=Pet.ADOPTED)
        expired_pet = self.create_pet_custom_date(90, 10)

        pets = Pet.objects.get_staled_pets()

        self.assertEqual(2, len(pets))
        self.assertIn(staled_missing_pet, pets)
        self.assertIn(staled_adoption_pet, pets)
        self.assertNotIn(staled_found_pet, pets)
        self.assertNotIn(staled_adopted_pet, pets)
        self.assertNotIn(new_missing_pet, pets)
        self.assertNotIn(new_adoption_pet, pets)
        self.assertNotIn(expired_pet, pets)

    def test_expired_pets(self):
        """Should return active pets with request_sent date older than expected"""
        new_pet = mommy.make(Pet)
        staled_pet = self.create_pet_custom_date(90)
        expired_pet = self.create_pet_custom_date(90, 90, active=True)
        inactive_expired_pet = self.create_pet_custom_date(90, 90, active=False)

        pets = Pet.objects.get_expired_pets()

        self.assertEqual(1, len(pets))
        self.assertIn(expired_pet, pets)
        self.assertNotIn(new_pet, pets)
        self.assertNotIn(staled_pet, pets)
        self.assertNotIn(inactive_expired_pet, pets)

    @patch('meupet.services.send_request_action_email')
    def test_request_action_from_user(self, mock_send_email):
        """Should call send_request_action_email method from request_action"""
        pet = mommy.make(Pet)
        pet.request_action()

        mock_send_email.assert_called_once_with(pet)

    @patch('meupet.services.send_deactivate_email')
    def test_deactivate_send_email(self, mock_send_email):
        """
        Deactivate should call the send_deactivate_email method
        """
        pet = mommy.make(Pet)
        pet.deactivate()

        mock_send_email.assert_called_once_with(pet)

    @patch('meupet.services.send_request_action_email')
    def test_request_sent_saved(self, mock_send_email):
        """Should set the request_sent date in the pet and keep modified date"""
        mock_send_email.return_value = True
        pet = mommy.make(Pet)
        modified = pet.modified

        pet.request_action()
        pet.refresh_from_db()

        self.assertIsNotNone(pet.request_sent)
        self.assertEqual(modified, pet.modified)
        self.assertAlmostEqual(pet.request_sent, timezone.now(), delta=timezone.timedelta(seconds=1))

    @patch('meupet.services.send_request_action_email')
    def test_request_action_email_set_activation_success(self, mock_send_email):
        """Should set the request_key if the send_request_action_email succeed"""
        mock_send_email.return_value = True
        pet = mommy.make(Pet, request_key='')

        pet.request_action()
        pet.refresh_from_db()

        self.assertNotEqual('', pet.request_key)

    def test_request_action_email_not_set_activation_fail(self):
        """Shouldn't set the request_key if the send_request_action_email fail"""
        pet = mommy.make(Pet, request_key='')

        with patch('meupet.services.send_request_action_email') as mock_method:
            mock_method.return_value = False
            pet.request_action()

        pet.refresh_from_db()

        self.assertEqual('', pet.request_key)

    @patch('meupet.services.send_deactivate_email')
    def test_deactivate(self, mock_send_email):
        """Should set the registration as inactive and keep modified date"""
        mock_send_email.return_value = True
        pet = mommy.make(Pet)
        modified = pet.modified

        pet.deactivate()
        pet.refresh_from_db()

        self.assertFalse(pet.active)
        self.assertEqual(modified, pet.modified)

    def test_activate(self):
        """Should set the registration to active and clear fields"""
        pet = mommy.make(Pet, active=False, request_key='abc', request_sent=timezone.now())

        pet.activate()
        pet.refresh_from_db()

        self.assertIsNone(pet.request_sent)
        self.assertEqual('', pet.request_key)
        self.assertTrue(pet.active)

    def test_get_active_pets(self):
        """Should return only active pets"""
        inactive_pet = mommy.make(Pet, active=False)
        missing_active = mommy.make(Pet, status=Pet.MISSING)
        adoption_active = mommy.make(Pet, status=Pet.FOR_ADOPTION)

        pets = Pet.objects.actives()

        self.assertIn(missing_active, pets)
        self.assertIn(adoption_active, pets)
        self.assertNotIn(inactive_pet, pets)

    @staticmethod
    def create_pet_custom_date(modified_days, request_sent_days=None, **kwargs):
        now = timezone.now()
        pet = mommy.make(Pet, **kwargs)
        pet.modified = now - timezone.timedelta(days=modified_days)
        if request_sent_days:
            pet.request_sent = now - timezone.timedelta(days=request_sent_days)
        pet.save(update_modified=False)
        return pet
