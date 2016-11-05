from django.core.urlresolvers import reverse

from meupet.models import Photo
from meupet.tests.tests import MeuPetTestCase


class PetDetailViewTest(MeuPetTestCase):
    def setUp(self):
        super(PetDetailViewTest, self).setUp()

        self.pet = self.create_pet('Pet')

    def test_get_pet_by_pk(self):
        resp = self.client.get(reverse('meupet:detail', kwargs={'pk_or_slug': self.pet.id}))

        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Testing Pet')

    def test_get_pet_by_slug(self):
        resp = self.client.get(reverse('meupet:detail', kwargs={'pk_or_slug': self.pet.slug}))

        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'Testing Pet')

    def test_show_more_photos_in_pet_detail(self):
        photo = Photo(image=self.get_test_image_file())
        self.pet.photo_set.add(photo)
        self.pet.save()

        response = self.client.get(self.pet.get_absolute_url())

        self.assertContains(response, 'Outras fotos')

    def test_show_404_not_found(self):
        """Show the default 404 page if the pet could not be found"""
        resp = self.client.get(reverse('meupet:detail', kwargs={'pk_or_slug': '404-pet'}))

        self.assertContains(resp, 'Página não encontrada')
