from unittest import mock

from model_mommy import mommy

from django.core.management import call_command
from django.test import TestCase

from common.models import Configuration


class RefreshFacebookTokenTest(TestCase):
    @mock.patch("requests.get")
    def test_refresh_token(self, mock_requests):
        configuration = mommy.make(Configuration, fb_share_token="123")
        mock_requests.return_value = mock.Mock(json=mock.Mock(return_value={"access_token": "321"}))

        call_command("refresh_facebook_token")

        mock_requests.assert_called()
        configuration.refresh_from_db()
        self.assertEqual(configuration.fb_share_token, "321")
