from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase

from users.forms import RegisterForm, UpdateUserForm
from users.validators import validate_facebook_url
from .models import OwnerProfile


class UserRegistrationTest(TestCase):
    def login_new_user(self):
        self.create_user()
        self.client.login(username='tester', password='test123')

    def create_user(self, username='tester'):
        user = OwnerProfile(first_name='Test First Name', last_name='Tester', email='te@ste.com',
                            username=username, is_information_confirmed=True)
        user.set_password('test123')
        user.save()
        return user

    def test_create_user(self):
        self.create_user()

        user = OwnerProfile.objects.first()

        self.assertEqual(OwnerProfile.objects.count(), 1)
        self.assertEqual('Test First Name', user.first_name)
        self.assertEqual('Tester', user.last_name)
        self.assertEqual('tester', user.username)
        self.assertTrue(user.check_password('test123'))

    def test_authenticate_with_recent_user(self):
        self.create_user()

        self.client.login(username='tester', password='test123')

        response = self.client.get('/')
        self.assertContains(response, 'Cadastrar Pet')

    def test_render_own_profile(self):
        self.login_new_user()

        response = self.client.get('/user/profile/')

        self.assertContains(response, 'Test First Name')
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_show_profile_link_if_logged(self):
        self.login_new_user()

        response = self.client.get('/')

        self.assertContains(response, 'Seu Perfil')

    def test_show_profile_information_for_logged_user(self):
        self.login_new_user()

        response = self.client.get('/user/profile/')

        self.assertContains(response, 'Test First Name')

    def test_edit_view_show_form_for_update_profile_information(self):
        self.login_new_user()

        response = self.client.get('/user/profile/edit/')

        self.assertContains(response, 'Gravar Alterações')
        self.assertContains(response, 'Editando Perfil')

    def test_edit_view_render_correct_template(self):
        self.login_new_user()

        response = self.client.get('/user/profile/edit/')

        self.assertTemplateUsed(response, 'users/edit_profile.html')

    def test_render_profile_with_correct_template(self):
        user = self.create_user()

        response = self.client.get(user.get_absolute_url())

        self.assertTemplateUsed('users/profile.html')
        self.assertContains(response, 'Test First Name')

    def test_login_after_create_account(self):
        response = self.client.post(
            '/user/', {
                'first_name': 'Name',
                'last_name': 'Last Name',
                'email': 'email@email.com',
                'username': 'pythonicuser',
                'password1': '123',
                'password2': '123'},
            follow=True
        )

        self.assertTemplateUsed(response, 'meupet/index.html')
        self.assertContains(response, 'Logout')

    def test_wrong_user_pass_display_error_on_login(self):
        response = self.client.post(
            '/user/login/', {
                'username': 'admin',
                'password': 'adminho',
            },
            follow=True
        )
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'nonfield')

    def test_user_account_without_social_login_should_be_confirmed_by_default(self):
        self.client.post(
            '/user/', {
                'first_name': 'Test',
                'last_name': 'Testing',
                'email': 'email@email.com',
                'username': 'pythonicuser',
                'password1': '123',
                'password2': '123'},
            follow=True
        )

        user = OwnerProfile.objects.first()

        self.assertEquals(user.first_name, 'Test')
        self.assertEquals(user.last_name, 'Testing')
        self.assertTrue(user.is_information_confirmed)

    def test_validator_facebook_profile_url(self):
        validate_facebook_url('https://www.facebook.com/4')
        self.assertRaises(ValidationError, validate_facebook_url, 'test@gmail.com')

    def test_cant_save_user_invalid_facebook_url(self):
        user = self.create_user()
        user.facebook = 'a'
        with self.assertRaises(ValidationError):
            user.save()
            user.full_clean()

    def test_show_facebook_url_profile_view_if_present(self):
        user_with_url = self.create_user()
        user_with_url.facebook = 'https://www.facebook.com/test'
        user_with_url.save()

        user_without_url = self.create_user(username='tester2')

        response_without_url = self.client.get(user_without_url.get_absolute_url())
        response_with_url = self.client.get(user_with_url.get_absolute_url())

        self.assertContains(response_without_url, 'Facebook', 0)
        self.assertContains(response_with_url, 'Facebook', 1)

    def test_only_logged_user_can_edit_profile(self):
        edit_url = reverse('users:edit')
        redirect_url = '{0}?next={1}'.format(reverse('users:login'), reverse('users:edit'))

        response = self.client.get(edit_url, follow=True)

        self.assertTemplateUsed(response, 'users/login.html')
        self.assertRedirects(response, redirect_url)

    def test_redirect_logged_user_to_next(self):
        self.create_user()
        url = '{}?next={}'.format(reverse('users:login'), reverse('meupet:register'))

        response = self.client.post(
            url, {
                'username': 'tester',
                'password': 'test123',
            },
            follow=True
        )

        self.assertRedirects(response, reverse('meupet:register'))

    def test_logged_user_cant_create_account(self):
        """Authenticated user must not access the form for account creation"""
        self.login_new_user()
        response = self.client.get(reverse('users:create'))

        self.assertRedirects(response, reverse('meupet:index'))


class UserDetailViewTest(TestCase):
    def test_show_information_on_profile(self):
        self.user = OwnerProfile.objects.create_user(
            first_name='Test First Name',
            last_name='Tester',
            email='te@ste.com',
            username='first_user',
            is_information_confirmed=True,
            phone='(99) 99999-9999'
        )

        self.resp = self.client.get(self.user.get_absolute_url())

        contents = [
            'Test First Name',
            'Tester',
            'te@ste.com',
            '(99) 99999-9999'
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)


class UserCreateViewTest(TestCase):
    def test_show_form_inputs(self):
        resp = self.client.get(reverse('users:create'))

        contents = [
            'name="first_name"',
            'name="last_name"',
            'name="email"',
            'name="username"',
            'name="facebook"',
            'name="phone"',
            'name="password1"',
            'name="password2"',
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(resp, expected)


class RegisterFormTest(TestCase):
    def test_form_has_fields(self):
        form = RegisterForm()
        expected = ['first_name', 'last_name', 'email', 'username',
                    'facebook', 'phone', 'password1', 'password2', ]

        self.assertSequenceEqual(expected, list(form.fields))


class UpdateUserFormTest(TestCase):
    def test_form_has_fields(self):
        form = UpdateUserForm()
        expected = ['first_name', 'last_name', 'email', 'facebook', 'phone', ]

        self.assertSequenceEqual(expected, list(form.fields))
