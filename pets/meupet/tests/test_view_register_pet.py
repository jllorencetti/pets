import tempfile

from django.core.urlresolvers import reverse
from django.test import override_settings

from model_mommy import mommy

from cities.models import City
from meupet.models import Pet
from meupet.models import Kind
from meupet.tests.tests import MEDIA_ROOT, MeuPetTestCase
from users.models import OwnerProfile


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
        self.kind = Kind.objects.create(kind='Test Kind')
        self.city = mommy.make(City, name='Testing City')
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.image = self._create_image()

    def tearDown(self):
        self.image.close()

    def test_show_registered_page(self):
        """A thank you page should be shown after registering the pet"""
        response = self.client.post(reverse('meupet:register'),
                                    data={'name': 'Testing Fuzzy Boots',
                                          'description': 'My lovely cat',
                                          'state': self.city.state.code,
                                          'city': self.city.code,
                                          'kind': self.kind.id,
                                          'status': Pet.MISSING,
                                          'profile_picture': self.image},
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meupet/registered.html')
