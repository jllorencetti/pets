from django.core.urlresolvers import reverse
from django.test import override_settings

from meupet.models import Kind
from meupet.models import Pet
from meupet.tests.tests import MEDIA_ROOT, MeuPetTestCase
from users.models import OwnerProfile


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class RegisteredViewTest(MeuPetTestCase):
    def setUp(self):
        self.kind = Kind.objects.create(kind='Test Kind')
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.pet = Pet.objects.create(name='Test pet', profile_picture=self.get_test_image_file(),
                                      owner=self.admin, kind=self.kind, status=Pet.MISSING)

    def test_html_registered_page(self):
        contents = [
            'Obrigado',
            'https://www.facebook.com/sharer.php?u=http://cademeubicho.com/pets/{}/'.format(self.pet.slug),
            'https://twitter.com/share?url=http://cademeubicho.com/pets/{}/'.format(self.pet.slug),
            reverse('meupet:detail', args=[self.pet.slug])
        ]

        response = self.client.get(reverse('meupet:registered', args=[self.pet.slug]))

        for expected in contents:
            with self.subTest():
                self.assertContains(response, expected)
