from unittest.mock import MagicMock, patch

from django.test import TestCase

from meupet.management.commands.shareonfacebook import Command
from meupet.models import Pet, City
from users.models import OwnerProfile


class ManagementCommandTest(TestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.city = City.objects.create(city='Araras')
        self.pet = Pet.objects.create(
            name='Testing Pet',
            city=self.city,
            status=Pet.MISSING,
            owner=self.admin
        )

    def test_shareonfacebook_command(self):
        link = {
            'link': 'http://www.test.com/{}'.format(self.pet.get_absolute_url())
        }

        mock = self.call_mocked_command(link)

        expected = 'Desaparecido: Testing Pet, Araras'
        mock.assert_called_once_with(expected, attachment=link)

    def call_mocked_command(self, link):
        mock = MagicMock()
        mock.get_renewed_token.return_value = 'token'
        mock.get_attachment.return_value = link

        cmd = Command()

        cmd.get_attachment = mock.get_attachment
        cmd.get_renewed_token = mock.get_renewed_token

        with patch('facebook.GraphAPI.put_wall_post') as mock:
            cmd.handle()
            return mock
