from django.core.urlresolvers import reverse
from django.test import override_settings

from model_mommy import mommy

from meupet.models import Pet
from meupet.tests.tests import MeuPetTestCase, MEDIA_ROOT


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PosterTest(MeuPetTestCase):
    def setUp(self):
        super().setUp()
        self.admin.phone = '99 99999-9999'
        self.admin.save()
        self.pet = mommy.make(Pet, owner=self.admin)
        self.resp = self.client.get(reverse('meupet:poster', kwargs={'slug': self.pet.slug}))

    def test_template_used(self):
        """Makes sure the correct template is used"""
        self.assertTemplateUsed(self.resp, 'meupet/poster.html')

    def test_pet_in_context(self):
        """The pet should be present in the context"""
        pet = self.resp.context['pet']
        self.assertIsInstance(pet, Pet)

    def test_poster_info(self):
        """Pet information should be presented in the poster"""
        contents = [
            self.pet.get_status_display(),
            self.pet.name,
            self.pet.description,
            self.pet.get_sex_display().lower(),
            self.pet.get_size_display().lower(),
            self.pet.owner.phone,
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)
