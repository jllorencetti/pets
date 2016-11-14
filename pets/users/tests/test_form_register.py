from django.test import TestCase

from users.forms import RegisterForm


class RegisteFormTest(TestCase):
    def test_form_has_fields(self):
        """Form should have the correct fields"""
        form = RegisterForm()

        expected = ['first_name', 'last_name', 'email', 'username',
                    'facebook', 'phone', 'password1', 'password2']

        self.assertSequenceEqual(expected, list(form.fields))

    def test_form_validates_facebook_url(self):
        """Form should execute at least a basic validation of the Facebook URL field"""
        form = self.make_validated_form(facebook='www.example.com')

        self.assertEqual(form.errors.as_data()['facebook'][0].message,
                         'Por favor, insira uma URL válida do seu perfil no Facebook.')

    def test_form_validate_passwords(self):
        """Both passwords provided by the user should be equal"""
        form = self.make_validated_form(password1='a', password2='b')

        self.assertEqual(form.errors.as_data()['password2'][0].message,
                         'Os dois campos de senha não combinam.')

    @staticmethod
    def make_validated_form(**kwargs):
        valid = dict(
            first_name='Admin',
            last_name='Adminson',
            email='admin@example.com',
            username='admin',
            facebook='https://www.facebook.com/adminadminson',
            phone='99 9999-9999',
            password1='123456',
            password2='123456',
        )
        data = dict(valid, **kwargs)
        form = RegisterForm(data)
        form.is_valid()
        return form
