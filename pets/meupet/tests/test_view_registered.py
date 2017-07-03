from django.core.urlresolvers import reverse
from django.test import override_settings

from model_mommy import mommy

from meupet.models import Pet
from meupet.tests.tests import MEDIA_ROOT, MeuPetTestCase
from users.models import OwnerProfile


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class RegisteredViewTest(MeuPetTestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.pet = mommy.make(Pet, owner=self.admin)

    def test_html_registered_page(self):
        """Validate information shown after registering the pet"""
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
