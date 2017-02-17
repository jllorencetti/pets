from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from meupet.models import Pet


class ServicesTest(TestCase):
    def test_request_action_from_user(self):
        """
        Validate the information sent in the email
        """
        pet = mommy.make(Pet)
        pet.request_action()
        email = mail.outbox[0]
        current_site = Site.objects.get_current()

        pet_update_url = reverse('meupet:update_register', args=[pet.request_key])
        full_url = '%s%s' % (current_site.domain, pet_update_url)

        contents = [
            pet.name,
            pet.owner.first_name,
            str(settings.DAYS_TO_STALE_REGISTER),
            full_url,
            pet.get_status_display().lower(),
            current_site.name,
        ]

        for expected in contents:
            with self.subTest():
                self.assertIn(expected, email.body)

    def test_pet_deactivated(self):
        """
        Validates the information present in the email
        """
        pet = mommy.make(Pet)
        pet.deactivate()
        email = mail.outbox[0]
        current_site = Site.objects.get_current()

        contents = [
            pet.owner.first_name,
            current_site.name,
        ]

        for expected in contents:
            with self.subTest():
                self.assertIn(expected, email.body)
