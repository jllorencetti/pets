import tempfile

from django.shortcuts import resolve_url

from model_mommy import mommy

from meupet.models import Pet
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
        super().setUp()
        self.pet = mommy.make(Pet, owner=self.admin)
        self.image = self._create_image()

    def tearDown(self):
        self.image.close()

    def test_upload_image(self):
        """User should be able to upload more images to their pets"""
        self.client.login(username='admin', password='admin')

        resp = self.client.post(
            resolve_url('meupet:upload_image', self.pet.slug),
            data={
                'another_picture': self.image
            },
            follow=True
        )

        self.assertTemplateUsed(resp, 'meupet/pet_detail.html')
        self.assertContains(resp, 'More photos')

    def test_upload_image_other_user(self):
        """Only the owner should be able to upload images to the pet"""
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
        self.assertNotContains(resp, 'More fotos')
