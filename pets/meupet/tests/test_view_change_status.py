from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from meupet.models import Pet
from users.models import OwnerProfile


class ChangeStatusViewTest(TestCase):
    def setUp(self):
        super(ChangeStatusViewTest, self).setUp()

        self.admin = OwnerProfile.objects.create_user(
            username='admin',
            password='admin',
        )
        self.pet = mommy.make(Pet, status=Pet.FOR_ADOPTION, owner=self.admin)

    def test_change_status(self):
        """Updates status of the pet from 'For Adoption' to 'Adopted'"""
        self.client.login(username='admin', password='admin')

        self.client.post(reverse('meupet:change_status', args=[self.pet.slug]))

        self.pet.refresh_from_db()

        self.assertEqual(Pet.ADOPTED, self.pet.status)

    def test_only_owner_can_update_pet(self):
        """Only the ownser should be able to change the pet's status"""
        response = self.client.post(reverse('meupet:change_status', args=[self.pet.slug]))

        self.pet.refresh_from_db()

        self.assertEqual(Pet.FOR_ADOPTION, self.pet.status)
        self.assertRedirects(response, self.pet.get_absolute_url())

    def test_only_accept_post_method(self):
        """View should only accept http POST method"""
        response = self.client.get(reverse('meupet:change_status', args=[self.pet.slug]))

        self.assertEqual(405, response.status_code)
