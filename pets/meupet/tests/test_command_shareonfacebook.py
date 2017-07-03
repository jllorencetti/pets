from unittest.mock import MagicMock, patch

from django.test import TestCase

from model_mommy import mommy

from cities.models import City
from meupet.management.commands.shareonfacebook import Command
from meupet.models import Pet
from users.models import OwnerProfile


class ManagementCommandTest(TestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.city = mommy.make(City, name='Araras')
        self.pet = mommy.make(Pet, city=self.city)
        self.url = 'http://www.test.com{}'

    def test_get_attachment(self):
        """The attachment should be a dict with the 'link' key
        being the absolute url to the pet"""
        attach = Command.get_attachment(self.pet, self.url)

        expected = self.url.format(self.pet.get_absolute_url())

        self.assertEqual(expected, attach.get('link', ''))

    def test_get_message(self):
        """The message in the post should always contains the
        display status, the name of the pet, and the name of the city"""
        msg = Command.get_message(self.pet)

        expected = '{0}: {1}, {2}'.format(self.pet.get_status_display(), self.pet.name, self.pet.city)

        self.assertEqual(expected, msg)

    def test_shareonfacebook_command(self):
        """The command should be called with the correct
        message and attachment"""
        mock = self.call_mocked_command()

        attach = Command.get_attachment(self.pet, self.url)
        msg = Command.get_message(self.pet)

        mock.assert_called_once_with(msg, attachment=attach)

    def call_mocked_command(self):
        mock = MagicMock()
        mock.fb_share_token = 'token'
        mock.fb_share_link = self.url

        cmd = Command()
        cmd.config = mock

        with patch('facebook.GraphAPI.put_wall_post') as mock:
            cmd.handle()
            return mock
