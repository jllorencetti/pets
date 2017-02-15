from unittest import mock

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from meupet.models import Pet


class DeactivateTestCase(TestCase):
    @staticmethod
    def test_deactivate_pets():
        """
        Command should call deactivate method in expired pets
        """
        request_sent = timezone.now() - timezone.timedelta(days=settings.DAYS_TO_STALE_REGISTER + 1)
        mommy.make(Pet, request_sent=request_sent)

        with mock.patch('meupet.models.Pet.deactivate') as mock_method:
            call_command('deactivate')

        mock_method.assert_any_call()
