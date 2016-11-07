from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from meupet.models import Pet
from users.models import OwnerProfile


class DeleteViewTest(TestCase):
    def setUp(self):
        super(DeleteViewTest, self).setUp()

        self.admin = OwnerProfile.objects.create_user(
            username='admin',
            password='admin',
        )
        self.pet = mommy.make(Pet, status=Pet.FOR_ADOPTION, owner=self.admin)

    def test_owner_can_delete_pet(self):
        """Only the owner should be able to delete its own pet"""
        self.client.login(username='admin', password='admin')

        response = self.client.post(reverse('meupet:delete_pet', args=[self.pet.slug]), follow=True)

        self.assertTemplateUsed(response, 'meupet/index.html')
        self.assertNotContains(response, self.pet.name)

    def test_user_cant_delete_pet_from_other(self):
        """Assert that an user can't delete pets from other people"""
        OwnerProfile.objects.create_user(username='other', password='user')
        self.client.login(username='other', password='user')

        response = self.client.post(reverse('meupet:delete_pet', args=[self.pet.slug]), follow=True)

        self.assertTemplateUsed(response, 'meupet/pet_detail.html')
        self.assertContains(response, self.pet.name)

    def test_only_accept_post_method(self):
        """View should only accept http POST method"""
        response = self.client.get(reverse('meupet:delete_pet', args=[self.pet.slug]))

        self.assertEqual(405, response.status_code)
