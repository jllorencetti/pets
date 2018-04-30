from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from meupet.models import Pet, PetStatus
from users.models import OwnerProfile


class ChangeStatusViewTest(TestCase):
    def setUp(self):
        super(ChangeStatusViewTest, self).setUp()

        self.admin = OwnerProfile.objects.create_user(
            username='admin',
            password='admin',
        )
        pet_status_next = mommy.make(PetStatus, final=True)
        pet_status = mommy.make(PetStatus, final=False, next_status=pet_status_next)
        self.pet = mommy.make(Pet, status=pet_status, owner=self.admin)

    def test_change_status(self):
        """Updates status of the pet from initial to a final status"""
        self.client.login(username='admin', password='admin')

        self.client.post(reverse('meupet:change_status', args=[self.pet.slug]))

        self.pet.refresh_from_db()

        self.assertTrue(self.pet.status.final)

    def test_only_owner_can_update_pet(self):
        """Only the ownser should be able to change the pet's status"""
        response = self.client.post(reverse('meupet:change_status', args=[self.pet.slug]))

        self.pet.refresh_from_db()

        self.assertFalse(self.pet.status.final)
        self.assertRedirects(response, self.pet.get_absolute_url())

    def test_only_accept_post_method(self):
        """View should only accept http POST method"""
        response = self.client.get(reverse('meupet:change_status', args=[self.pet.slug]))

        self.assertEqual(405, response.status_code)
