from django.test import TestCase

from users.forms import UsersPasswordResetForm


class UsersPasswordResetFormTest(TestCase):
    def test_submit_button_present(self):
        """Submit button should be present in the helper"""
        form = UsersPasswordResetForm(user=None)

        self.assertIn('Recover password', form.helper.inputs[0].value)
