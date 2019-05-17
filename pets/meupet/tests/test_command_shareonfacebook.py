from unittest.mock import MagicMock, patch

from model_mommy import mommy

from django.test import TestCase

from cities.models import City
from meupet.management.commands.shareonfacebook import Command
from meupet.models import Pet, PetStatus
from users.models import OwnerProfile


class ManagementCommandTest(TestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username="admin", password="admin")
        self.city = mommy.make(City, name="Araras")
        pet_status = mommy.make(PetStatus, final=False)
        self.pet = mommy.make(Pet, city=self.city, status=pet_status)
        self.url = "http://www.test.com{}"

    def test_get_message(self):
        """The message in the post should always contains the
        display status, the name of the pet, and the name of the city"""
        msg = Command.get_message(self.pet)

        expected = "{0}: {1}, {2}".format(self.pet.status.description, self.pet.name, self.pet.city)

        self.assertEqual(expected, msg)

    def test_shareonfacebook_command(self):
        """The command should be called with the correct
        message and attachment"""
        mock = self.call_mocked_command()

        msg = Command.get_message(self.pet)

        mock.assert_called_once_with(
            parent_object="me",
            connection_name="feed",
            message=msg,
            link=self.url.format(self.pet.get_absolute_url()),
        )

    def call_mocked_command(self):
        mock = MagicMock()
        mock.fb_share_token = "token"
        mock.fb_share_link = self.url

        cmd = Command()
        cmd.config = mock

        with patch("facebook.GraphAPI.put_object") as mock:
            cmd.handle()
            return mock
