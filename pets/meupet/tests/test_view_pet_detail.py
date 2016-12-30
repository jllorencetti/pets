from django.core.urlresolvers import reverse

from model_mommy import mommy

from meupet.models import Photo
from meupet.tests.tests import MeuPetTestCase


class PetDetailViewTest(MeuPetTestCase):
    def setUp(self):
        super(PetDetailViewTest, self).setUp()

        self.pet = self.create_pet()

    def test_get_pet_by_pk(self):
        """Show detail page using an id as a value to the 'pk_or_slug' argument"""
        resp = self.client.get(reverse('meupet:detail', kwargs={'pk_or_slug': self.pet.id}))

        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, self.pet.name)

    def test_get_pet_by_slug(self):
        """Show detail page using a slug as a value to the 'pk_or_slug' argument"""
        resp = self.client.get(reverse('meupet:detail', kwargs={'pk_or_slug': self.pet.slug}))

        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, self.pet.slug)

    def test_show_more_photos_in_pet_detail(self):
        """Show the 'More Photos' section if more photos are added"""
        photo = mommy.make(Photo)
        self.pet.photo_set.add(photo)
        self.pet.save()

        response = self.client.get(self.pet.get_absolute_url())

        self.assertContains(response, 'More photos')

    def test_show_404_not_found(self):
        """Show the default 404 page if the pet could not be found"""
        resp = self.client.get(reverse('meupet:detail', kwargs={'pk_or_slug': '404-pet'}))

        self.assertContains(resp, 'Página não encontrada', status_code=404)
