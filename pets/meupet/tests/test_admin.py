from django.core import mail

from meupet.admin import PetAdmin, admin
from meupet.models import Pet
from users.models import OwnerProfile
from .tests import MeuPetTestCase


class PetAdminTest(MeuPetTestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username='admin',
                                                      password='admin',
                                                      email='pets.adim@mailinator.com')
        self.model_admim = PetAdmin(Pet, admin.site)
        self.create_some_pets()

    def test_has_action(self):
        """Admin must have request_unsolvedcases_status action"""
        self.assertIn('request_unsolvedcases_status', self.model_admim.actions)

    def test_request_unsolvedcases_status_for_all(self):
        """It should request status for all pets"""
        self.call_action(Pet.objects.all())

    def test_request_unsolvedcases_status_for_first(self):
        """It should request status for the MISSING pets"""
        self.call_action(Pet.objects.filter(status=Pet.MISSING))

    def call_action(self, queryset):
        self.model_admim.request_unsolvedcases_status(None, queryset)
        self.assertTrue(len(mail.outbox) == len(queryset))
