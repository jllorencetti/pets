from django.shortcuts import resolve_url
from django.test import TestCase

from users.models import OwnerProfile


class ConfirmInformationTest(TestCase):
    def test_redirect_to_confirmation(self):
        """User not confirmed should be redirected to the edit page"""
        self.create_user(False)
        self.client.login(username='admin', password='test123')

        resp = self.client.get(resolve_url('users:confirm_information'))

        self.assertRedirects(resp, resolve_url('users:edit'))

    def test_redirect_to_index(self):
        """Confirmed user should be redirected to the index page"""
        self.create_user(True)
        self.client.login(username='admin', password='test123')

        resp = self.client.get(resolve_url('users:confirm_information'))

        self.assertRedirects(resp, resolve_url('meupet:index'))

    @staticmethod
    def create_user(is_confirmed):
        user = OwnerProfile(first_name='Admin', last_name='Adminson', email='admin@example.com',
                            username='admin', is_information_confirmed=is_confirmed)
        user.set_password('test123')
        user.save()
