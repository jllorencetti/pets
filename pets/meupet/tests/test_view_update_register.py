from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from meupet.models import Pet


class UpdateRegisterViewTest(TestCase):
    def setUp(self):
        stale_date = timezone.now() - timezone.timedelta(days=90)
        self.pet = mommy.make(Pet, request_sent=stale_date, active=False, request_key='abc')

    def test_redirect_to_pet(self):
        """Redirect to the detail view after updating the registration"""
        resp = self.client.get(reverse('meupet:update_register', args=[self.pet.request_key]))

        self.assertRedirects(resp, reverse('meupet:detail', args=[self.pet.slug]))

    def test_not_found(self):
        """Shows 404 if pet not found with given request_key"""
        resp = self.client.get(reverse('meupet:update_register', args=['cba']), follow=True)

        self.assertEqual(404, resp.status_code)
        self.assertTemplateUsed(resp, '404.html')

    def test_update_pet_registration(self):
        """Should set the registration as active"""
        self.client.get(reverse('meupet:update_register', args=[self.pet.request_key]))

        self.pet.refresh_from_db()

        self.assertTrue(self.pet.active)
