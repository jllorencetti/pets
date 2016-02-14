import shutil
import tempfile
from unittest.mock import MagicMock, patch

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.utils.timezone import now, timedelta

from meupet import forms
from meupet.management.commands.shareonfacebook import Command
from meupet.models import Pet, Kind, Photo, City
from users.models import OwnerProfile

from meupet.services import get_unsolved_cases_perdiod_range


def get_test_image_file():
    from django.core.files.images import ImageFile
    file = tempfile.NamedTemporaryFile(suffix='.png')
    return ImageFile(file, name=file.name)


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class MeuPetTest(TestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.test_city, _ = City.objects.get_or_create(city='Testing City')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def create_pet(self, kind, name='Pet', status=Pet.MISSING, **kwargs):
        image = get_test_image_file()
        user = self.admin
        kind = Kind.objects.get_or_create(kind=kind)[0]
        return Pet.objects.create(name='Testing ' + name, description='Bla',
                                  profile_picture=image, owner=user, kind=kind,
                                  status=status, **kwargs)

    def test_titleize_name(self):
        data = {
            'name': 'TESTING NAME'
        }
        form = forms.PetForm(data=data)
        form.is_valid()
        self.assertEquals(form.cleaned_data['name'], 'Testing Name')

    def test_display_all_pets(self):
        self.create_pet('Goat', 'Goat')
        self.create_pet('Cat', 'Cat')

        home = self.client.get(reverse('meupet:index'))

        self.assertContains(home, 'Testing Goat')
        self.assertContains(home, 'Testing Cat')

    def test_display_kinds_sidebar(self):
        Kind.objects.get_or_create(kind='0 Pets')
        self.create_pet('Goat')
        self.create_pet('Cat')

        home = self.client.get(reverse('meupet:index'))

        self.assertContains(home, 'Goat')
        self.assertContains(home, 'Cat')
        self.assertNotContains(home, '0 Pets')

    def test_display_only_pets_from_kind(self):
        self.create_pet('Goat', 'Goat')
        self.create_pet('Cat', 'Cat')
        self.create_pet('Cat', 'Costela')
        kind = Kind.objects.get(kind='Cat')

        content = self.client.get(reverse('meupet:lost', args=[kind.id]))
        pets_count = Pet.objects.filter(kind=kind).count()

        self.assertContains(content, 'Testing Cat')
        self.assertContains(content, 'Testing Costela')
        self.assertNotContains(content, 'Testing Goat')
        self.assertEqual(2, pets_count)

    def test_show_edit_button_for_own_if_logged_pet(self):
        pet = self.create_pet('Own Pet')
        self.client.login(username='admin', password='admin')

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Editar')
        self.assertContains(response, reverse('meupet:edit', args=[pet.id]))

    def test_load_data_for_editing_pet(self):
        pet = self.create_pet('Own Pet', 'Own Pet')
        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('meupet:edit', args=[pet.id]))

        self.assertTemplateUsed(response, 'meupet/edit.html')
        self.assertContains(response, 'Testing Own Pet')
        self.assertContains(response, 'Bla')
        self.assertContains(response, 'Salvar Alterações')

    def test_owner_can_delete_pet(self):
        pet = self.create_pet('Own Pet')
        self.client.login(username='admin', password='admin')

        response = self.client.post(reverse('meupet:delete_pet', args=[pet.id]), follow=True)

        self.assertTemplateUsed(response, 'meupet/index.html')
        self.assertNotContains(response, 'Testing Pet')

    def test_other_user_can_delete_pet(self):
        pet = self.create_pet('Own Pet')
        OwnerProfile.objects.create_user(username='other', password='user')
        self.client.login(username='other', password='user')

        response = self.client.post(reverse('meupet:delete_pet', args=[pet.id]), follow=True)

        self.assertTemplateUsed(response, 'meupet/pet_detail.html')
        self.assertContains(response, 'Testing Pet')

    def test_can_edit_pet(self):
        pet = self.create_pet('Own Pet')
        kind = Kind.objects.first()
        self.client.login(username='admin', password='admin')
        url = Pet.objects.first().profile_picture.url

        response_post = self.client.post(reverse('meupet:edit', args=[pet.id]),
                                         data={'name': 'Testing Fuzzy Boots',
                                               'description': 'My lovely cat',
                                               'city': self.test_city.id,
                                               'kind': kind.id,
                                               'status': pet.status,
                                               'profile_picture': url})
        response_get = self.client.get(pet.get_absolute_url())

        self.assertRedirects(response_post, pet.get_absolute_url())
        self.assertContains(response_get, 'Testing Fuzzy Boots')

    def test_show_facebook_only_if_registered(self):
        self.create_pet('Own Pet', 'Own Pet')
        self.create_pet('Second Pet', 'Second Pet')
        user = OwnerProfile.objects.create_user(username='second_user', password='admin')
        user.facebook = 'http://www.facebook.com/owner_profile'
        user.save()
        pet = Pet.objects.first()
        pet.owner = user
        pet.save()

        resp_with_facebook = self.client.get(pet.get_absolute_url())

        self.assertContains(resp_with_facebook, 'http://www.facebook.com/owner_profile')

    def test_show_link_for_owner_profile(self):
        pet = self.create_pet('Pet')

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, reverse('users:user_profile', args=[self.admin.id]))

    def test_should_redirect_if_not_confirmed(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('meupet:register'))

        self.assertRedirects(response, '/user/profile/edit/')

    def test_should_access_if_confirmed(self):
        admin = OwnerProfile.objects.first()
        admin.is_information_confirmed = True
        admin.save()
        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('meupet:register'))

        self.assertTemplateUsed(response, 'meupet/register_pet.html')

    def test_only_owner_can_see_edit_page(self):
        OwnerProfile.objects.create_user(username='Other User', password='otherpass')
        pet = self.create_pet('Own Pet')
        self.client.login(username='Other User', password='otherpass')

        response = self.client.get(reverse('meupet:edit', args=[pet.id]))

        self.assertRedirects(response, pet.get_absolute_url())

    def test_display_status_on_pet_page(self):
        missing_pet = self.create_pet('Test', 'Test 1')
        adoption_pet = self.create_pet('Test', 'Test 2', status=Pet.FOR_ADOPTION)

        response_missing = self.client.get(missing_pet.get_absolute_url())
        response_adoption = self.client.get(adoption_pet.get_absolute_url())

        self.assertContains(response_missing, 'Test 1 - Desaparecido')
        self.assertContains(response_adoption, 'Test 2 - Para Adoção')

    def test_manager_lost_found(self):
        missing_pet = self.create_pet('Test')
        self.create_pet('Test')
        self.create_pet('Test', status=Pet.FOUND)
        self.create_pet('Test', status=Pet.FOR_ADOPTION)

        pets = Pet.objects.get_lost_or_found(missing_pet.kind.id)

        self.assertEquals(len(pets), 3)

    def test_manager_adoption_adopted(self):
        adopted_pet = self.create_pet('Test', status=Pet.ADOPTED)
        self.create_pet('Test')
        self.create_pet('Test', status=Pet.FOUND)
        self.create_pet('Test', status=Pet.FOR_ADOPTION)

        pets = Pet.objects.get_for_adoption_adopted(adopted_pet.kind.id)

        self.assertEquals(len(pets), 2)

    def test_incorrect_form_submission_reload_page_with_values(self):
        self.client.login(username='admin', password='admin')

        response = self.client.post(reverse('meupet:register'),
                                    {'description': 'Test Description'},
                                    follow=True)

        self.assertContains(response, 'Test Description')

    def test_show_add_photo_button_in_pet_page_owner_logged_in(self):
        pet = self.create_pet('Cat')
        self.client.login(username='admin', password='admin')

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Adicionar Foto')
        self.assertContains(response, 'another_picture')

    def test_show_more_photos_in_pet_detail(self):
        photo = Photo(image=get_test_image_file())
        pet = self.create_pet('Cat')
        pet.photo_set.add(photo)
        pet.save()

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Outras fotos')

    def test_search_pet(self):
        self.create_pet('Cat', city=self.test_city, size=Pet.SMALL)

        response_name = self.client.get(reverse('meupet:quick_search'), {'q': 'Testing'})
        response_desc = self.client.get(reverse('meupet:quick_search'), {'q': 'bla'})
        response_city = self.client.get(reverse('meupet:quick_search'), {'q': self.test_city})
        response_size = self.client.get(reverse('meupet:quick_search'), {'q': 'Pequeno'})

        self.assertContains(response_name, 'Testing Pet')
        self.assertContains(response_desc, 'Testing Pet')
        self.assertContains(response_city, self.test_city)
        self.assertContains(response_size, 'Testing Pet')

    def test_show_city(self):
        pet = self.create_pet('Cat')
        pet.city = self.test_city
        pet.save()

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, self.test_city)

    def test_show_size(self):
        pet = self.create_pet('Cat', size=Pet.SMALL)

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Pequeno')

    def test_empty_quicksearch_show_suggestion_to_advanced_search(self):
        response = self.client.get(reverse('meupet:quick_search'), {'q': ''})

        self.assertTemplateUsed(response, 'meupet/quicksearch.html')
        self.assertContains(response, 'Nenhum animalzinho encontrado')
        self.assertContains(response, reverse('meupet:search'), 2)

    def test_quicksearch_should_return_pet(self):
        self.create_pet('Dog')

        response = self.client.get(reverse('meupet:quick_search'), {'q': 'Pet'})

        self.assertContains(response, 'Testing Pet')

    def test_custom_search_without_filters(self):
        response = self.client.post(reverse('meupet:search'), {})

        self.assertContains(response, 'É necessário selecionar ao menos um filtro')

    def test_custom_search_with_filter(self):
        pet = self.create_pet('Dog', city=self.test_city)

        response = self.client.post(reverse('meupet:search'), {'city': self.test_city.id}, follow=True)

        self.assertContains(response, pet.name)
        self.assertContains(response, pet.city)

    def test_show_pet_sex(self):
        pet = self.create_pet('Dog', sex=Pet.FEMALE)

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Fêmea')

    def test_change_status_and_show_status_label(self):
        pet = self.create_pet('Dog', status=Pet.FOR_ADOPTION)
        self.client.post(reverse('meupet:change_status', args=[pet.id]))

        response = self.client.get(reverse('meupet:index'))

        self.assertContains(response, '<h2 class="text-center"><span>Adotado! :)</span></h2>')

    def test_get_pets_unpublished(self):
        pet = self.create_pet('Dog')

        pets = Pet.objects.get_unpublished_pets()

        self.assertIn(pet, pets)

    def test_dont_get_published_pet(self):
        pet = self.create_pet('Dog', published=True)

        pets = Pet.objects.get_unpublished_pets()

        self.assertNotIn(pet, pets)

    def test_get_unsolved_cases_exists(self):
        """Test if get_unsolved_cases method exists in PetManager"""
        self.assertTrue(hasattr(Pet.objects.get_unsolved_cases, '__call__'))

    def test_get_unsolved_cases_return(self):
        """get_unsolved_cases method must return opened cases"""
        self.create_pet('Dog', 'Pet1', Pet.ADOPTED)
        self.create_pet('Bird', 'Pet2', Pet.ADOPTED)
        self.create_pet('Cat', 'Pet3', Pet.MISSING)
        self.create_pet('Dog', 'Pet4', Pet.FOR_ADOPTION)

        unsolved_cases = Pet.objects.get_unsolved_cases()

        self.assertEqual(len(unsolved_cases), 2)

    def test_get_unsolved_cases_perdiod_range(self):
        """get_unsolved_cases_perdiod_range service must return period start and end"""
        today = now()
        today_3months_ago = today - timedelta(days=90)

        period_range = get_unsolved_cases_perdiod_range(today)

        self.assertTrue(period_range[0] == today_3months_ago)
        self.assertTrue(period_range[1] == today)

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PetRegisterTest(TestCase):
    def _create_image(self):
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

    def setUp(self):
        self.kind = Kind.objects.create(kind='Test Kind')
        self.city = City.objects.create(city='Testing City')
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.image = self._create_image()

    def tearDown(self):
        self.image.close()

    def test_show_registered_page(self):
        """A thank you page should be shown after registering the pet"""
        response = self.client.post(reverse('meupet:register'),
                                    data={'name': 'Testing Fuzzy Boots',
                                          'description': 'My lovely cat',
                                          'city': self.city.id,
                                          'kind': self.kind.id,
                                          'status': Pet.MISSING,
                                          'profile_picture': self.image},
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meupet/registered.html')


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class RegisteredViewTest(TestCase):
    def setUp(self):
        self.kind = Kind.objects.create(kind='Test Kind')
        self.admin = OwnerProfile.objects.create_user(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.pet = Pet.objects.create(name='Test pet', profile_picture=get_test_image_file(),
                                      owner=self.admin, kind=self.kind, status=Pet.MISSING)

    def test_html_registered_page(self):
        contents = [
            'Obrigado',
            'https://www.facebook.com/sharer.php?u=http://cademeubicho.com/pets/{}/'.format(self.pet.id),
            'https://twitter.com/share?url=http://cademeubicho.com/pets/{}/'.format(self.pet.id),
            reverse('meupet:detail', args=[self.pet.id])
        ]

        response = self.client.get(reverse('meupet:registered', args=[self.pet.id]))

        for expected in contents:
            with self.subTest():
                self.assertContains(response, expected)


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
