import tempfile

from django.shortcuts import resolve_url

from meupet.models import Pet, City
from meupet.tests.tests import MeuPetTestCase
from users.models import OwnerProfile


class UploadImageTestCase(MeuPetTestCase):
    @staticmethod
    def _create_image():
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

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
            description='Testing Pet',
            size=Pet.MEDIUM,
            sex=Pet.MALE,
            profile_picture=self.get_test_image_file()
        )
        self.image = self._create_image()

    def tearDown(self):
        self.image.close()

    def test_upload_image(self):
        self.client.login(username='admin', password='admin')

        resp = self.client.post(
            resolve_url('meupet:upload_image', self.pet.slug),
            data={
                'another_picture': self.image
            },
            follow=True
        )

        self.assertTemplateUsed(resp, 'meupet/pet_detail.html')
        self.assertContains(resp, 'Outras fotos')

    def test_upload_image_other_user(self):
        OwnerProfile.objects.create_user(
            username='other',
            password='other',
        )

        self.client.login(username='other', password='other')

        resp = self.client.post(
            resolve_url('meupet:upload_image', self.pet.slug),
            data={
                'another_picture': self.image
            },
            follow=True
        )

        self.assertTemplateUsed(resp, 'meupet/pet_detail.html')
        self.assertNotContains(resp, 'Outras fotos')
