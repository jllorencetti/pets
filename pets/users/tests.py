from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import OwnerProfile


class UserRegistrationTest(TestCase):
    def login_new_user(self):
        self.create_user()
        self.client.login(username='tester', password='test123')

    def create_user(self):
        user = OwnerProfile(first_name='Test First Name', last_name='Tester', email='te@ste.com',
                            username='tester')
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

        response = self.client.get(reverse('users:user_profile', args=[user.id]))

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
        self.assertContains(response, 'alert-danger')

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