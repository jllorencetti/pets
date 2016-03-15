from django.core.urlresolvers import reverse
from django.test import override_settings

from meupet.models import City, Pet
from meupet.tests.tests import MeuPetTestCase, MEDIA_ROOT
from users.models import OwnerProfile


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PosterTest(MeuPetTestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(
            username='admin',
            password='admin',
            phone='99 99999-9999'
        )
        self.city = City.objects.create(city='Test City')
        self.pet = Pet.objects.create(
            name='Testing Pet',
            city=self.city,
            status=Pet.MISSING,
            owner=self.admin,
            description='Lost imaginary pet',
            size=Pet.MEDIUM,
            sex=Pet.MALE,
            profile_picture=self.get_test_image_file()
        )
        self.resp = self.client.get(reverse('meupet:poster', kwargs={'slug': self.pet.slug}))

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'meupet/poster.html')

    def test_pet_in_context(self):
        pet = self.resp.context['pet']
        self.assertIsInstance(pet, Pet)

    def test_poster_info(self):
        contents = [
            'Desaparecido',
            'Testing Pet',
            'Lost imaginary pet',
            'Porte médio, macho',
            '99 99999-9999'
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)
