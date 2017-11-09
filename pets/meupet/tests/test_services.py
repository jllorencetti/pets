from unittest import mock

from django.conf import settings
from django.contrib.sites.models import Site
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

        with mock.patch('meupet.services.send_email') as mock_send_email:
            pet.request_action()

        current_site = Site.objects.get_current()
        pet_update_url = reverse('meupet:update_register', args=[pet.request_key])
        context = {
            'username': pet.owner.first_name,
            'pet': pet.name,
            'days': settings.DAYS_TO_STALE_REGISTER,
            'status': pet.get_status_display().lower(),
            'link': 'https://%s%s' % (current_site.domain, pet_update_url),
            'site_name': current_site.name,
        }

        mock_send_email.assert_called_once_with(
            'Update pet registration',
            pet.owner.email,
            'meupet/request_action_email.txt',
            context
        )

    def test_pet_deactivated(self):
        """
        Validates the information present in the email
        """
        pet = mommy.make(Pet)

        with mock.patch('meupet.services.send_email') as mock_send_email:
            pet.deactivate()

        context = {
            'username': pet.owner.first_name,
            'site_name': Site.objects.get_current().name,
        }

        mock_send_email.assert_called_once_with(
            'Deactivation of pet registration',
            pet.owner.email,
            'meupet/deactivate_email.txt',
            context
        )
