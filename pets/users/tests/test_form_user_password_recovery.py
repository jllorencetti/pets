from django.test import TestCase

from users.forms import UsersPasswordRecoveryForm


class UsersPasswordRecoveryFormTest(TestCase):
    def test_username_email_label(self):
        """Label should be corrected configured"""
        form = UsersPasswordRecoveryForm()

        self.assertEqual(form['username_or_email'].label, '')

    def test_submit_button_present(self):
        """Submit button should be present in the helper"""
        form = UsersPasswordRecoveryForm()

        self.assertIn('Recover password', form.helper.inputs[0].value)
