from unittest import mock

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from meupet.models import Pet


class RequestActionTest(TestCase):
    @staticmethod
    def test_requestaction():
        """Command should call request_action in staled pets"""
        pet = mommy.make(Pet)
        pet.modified = timezone.now() - timezone.timedelta(days=settings.DAYS_TO_STALE_REGISTER)
        pet.save(update_modified=False)

        with mock.patch('meupet.models.Pet.request_action') as mock_method:
            call_command('requestaction')

        mock_method.assert_any_call()
