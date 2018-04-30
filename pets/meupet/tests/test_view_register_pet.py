import tempfile

from django.core.urlresolvers import reverse
from django.test import override_settings
from model_mommy import mommy

from meupet.models import Kind, PetStatus
from meupet.models import Pet
from meupet.tests.tests import MEDIA_ROOT, MeuPetTestCase


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PetRegisterTest(MeuPetTestCase):
    @staticmethod
    def _create_image():
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

    def setUp(self):
        super(PetRegisterTest, self).setUp()
        status = mommy.make(PetStatus)
        self.kind = Kind.objects.create(kind='Test Kind')
        self.client.login(username='admin', password='admin')
        self.image = self._create_image()
        self.pet_data = {
            'name': 'Testing Fuzzy Boots',
            'description': 'My lovely cat',
            'state': self.test_city.state.code,
            'city': self.test_city.code,
            'kind': self.kind.id,
            'status': status.id,
            'profile_picture': self.image
        }

    def tearDown(self):
        self.image.close()

    def test_show_registered_page(self):
        """A thank you page should be shown after registering the pet"""
        response = self.client.post(reverse('meupet:register'), data=self.pet_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meupet/registered.html')

    def test_cant_duplicate_pet(self):
        """Should redirect users to their profile page if they try to duplicate a pet"""
        self.create_pet(name=self.pet_data['name'])
        response = self.client.post(reverse('meupet:register'), data=self.pet_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
