import tempfile

from django.core import mail
from django.core.management import BaseCommand
from meupet.models import Pet, City, Kind
from users.models import OwnerProfile

from .tests import MeuPetTestCase

from meupet.management.commands.request_unsolvedcases_status import Command


class ManagementCommandRequestUnsolvedCases(MeuPetTestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username='admin',
                                                      password='admin',
                                                      email='pets.adim@mailinator.com')
        self.create_some_pets()
        self.cmd = Command()

    def test_cmd_request_unsolvedcases_status(self):
        """Must have a management cmd to request unsolved cases status"""
        self.assertIsInstance(self.cmd, BaseCommand)


    def test_cmd_request_unsolvedcases_sendmail(self):
        """Cmd must send e-mail"""
        self.cmd.handle()
        self.assertTrue(len(mail.outbox) > 0)
