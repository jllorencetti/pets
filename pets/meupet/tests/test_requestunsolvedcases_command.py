import tempfile

from django.core import mail
from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.core.management import BaseCommand
from meupet.models import Pet, City, Kind
from users.models import OwnerProfile

from meupet.management.commands.request_unsolvedcases_status import Command


class ManagementCommandRequestUnsolvedCases(TestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin', email='pauloromanocarvalho@gmail.com')
        today = now()
        today_2months_ago = now() - timedelta(days=60)
        today_4months_ago = now() - timedelta(days=120)
        self.create_pet('Cat', 'Pet1', Pet.MISSING, modified=today)
        self.create_pet('Dog', 'Pet2', Pet.FOR_ADOPTION, modified=today_2months_ago)
        self.create_pet('Cat', 'Pet3', Pet.MISSING, modified=today_4months_ago)
        self.create_pet('Dog', 'Pet4', Pet.FOR_ADOPTION, modified=today_4months_ago)
        self.cmd = Command()

    @staticmethod
    def get_test_image_file():
        from django.core.files.images import ImageFile
        file = tempfile.NamedTemporaryFile(suffix='.png')
        return ImageFile(file, name=file.name)

    def create_pet(self, kind, name='Pet', status=Pet.MISSING, **kwargs):
        image = self.get_test_image_file()
        user = self.admin
        kind = Kind.objects.get_or_create(kind=kind)[0]
        return Pet.objects.create(name='Testing ' + name, description='Bla',
                                  profile_picture=image, owner=user, kind=kind,
                                  status=status, **kwargs)

    def test_cmd_request_unsolvedcases_status(self):
        """Must have a management cmd to request unsolved cases status"""
        self.assertIsInstance(self.cmd, BaseCommand)


    def test_cmd_request_unsolvedcases_sendmail(self):
        """Cmd must send e-mail"""
        self.cmd.handle()
        self.assertTrue(len(mail.outbox) > 0)
