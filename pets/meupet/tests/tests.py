import shutil
import tempfile

from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from django.utils.text import slugify

from model_mommy import mommy

from cities.models import City
from meupet import forms
from meupet.models import Pet, Kind, PetStatus, StatusGroup
from meupet.views import paginate_pets
from users.models import OwnerProfile

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class MeuPetTestCase(TestCase):
    def setUp(self):
        self.admin = OwnerProfile.objects.create_user(
            username='admin',
            password='admin',
            facebook='http://www.facebook.com/owner_profile'
        )
        self.test_city = mommy.make(City, name='Testing City')

    def create_pet(self, status=None, kind=None, **kwargs):
        if not status:
            group = mommy.make(StatusGroup, )
            status = mommy.make(PetStatus, final=False, group=group)

        pet = mommy.make(Pet, status=status, owner=self.admin, **kwargs)

        if kind:
            kind, _ = Kind.objects.get_or_create(kind=kind, slug=slugify(kind))

            if kwargs.get('_quantity', None):
                for p in pet:
                    p.kind = kind
                    p.save()
            else:
                pet.kind = kind
                pet.save()

        return pet

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


class MeuPetTest(MeuPetTestCase):
    def test_titleize_name(self):
        """Force the case of the pet's name to be titleized"""
        data = {'name': 'TESTING NAME'}
        form = forms.PetForm(data=data)
        form.is_valid()
        self.assertEquals(form.cleaned_data['name'], 'Testing Name')

    def test_display_all_pets(self):
        """Display recently adds pets in the index page"""
        first_pet = self.create_pet()
        second_pet = self.create_pet()

        home = self.client.get(reverse('meupet:index'))

        self.assertContains(home, first_pet.name)
        self.assertContains(home, second_pet.name)

    def test_display_kinds_sidebar(self):
        """The side bar should show only kinds that have pets registered and active"""
        Kind.objects.get_or_create(kind='0 Pets')
        first_pet = self.create_pet(kind='Cat')
        second_pet = self.create_pet(kind='Dog')
        inactive_pet = self.create_pet(kind='Inactive', active=False)

        home = self.client.get(reverse('meupet:index'))

        self.assertContains(home, first_pet.kind.kind)
        self.assertContains(home, second_pet.kind.kind)
        self.assertNotContains(home, '0 Pets')
        self.assertNotContains(home, inactive_pet.kind.kind)

    def test_display_only_pets_from_kind(self):
        """Only display the actives pets from the kind being shown"""
        first_cat = self.create_pet(kind='Cat')
        second_cat = self.create_pet(kind='Cat', status=first_cat.status)
        inactive_cat = self.create_pet(kind='Cat', active=False)
        dog = self.create_pet(kind='Dog')

        kind = Kind.objects.get(kind='Cat')

        content = self.client.get(reverse('meupet:pet_list', args=[first_cat.status.group.slug, kind.slug]))
        pets_count = Pet.objects.actives().filter(kind=kind).count()

        self.assertContains(content, first_cat.name)
        self.assertContains(content, second_cat.name)
        self.assertNotContains(content, inactive_cat.name)
        self.assertNotContains(content, dog.name)
        self.assertEqual(2, pets_count)

    def test_show_edit_button_for_own_if_logged_pet(self):
        """Show the edit button only if the owner is logged in"""
        pet = self.create_pet()
        self.client.login(username='admin', password='admin')

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Edit')
        self.assertContains(response, reverse('meupet:edit', args=[pet.slug]))

    def test_load_data_for_editing_pet(self):
        """Assert that the saved data is being preloaded in the edit page"""
        pet = self.create_pet()
        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('meupet:edit', args=[pet.slug]))

        self.assertTemplateUsed(response, 'meupet/edit.html')
        self.assertContains(response, pet.name)
        self.assertContains(response, pet.description)
        self.assertContains(response, 'Save Changes')

    def test_can_edit_pet(self):
        """Pet's owner can edit it's own pet"""
        self.client.login(username='admin', password='admin')
        pet = self.create_pet(kind='Cat')

        response_post = self.client.post(
            reverse('meupet:edit', args=[pet.slug]),
            data={
                'name': 'Testing Fuzzy Boots',
                'description': 'My lovely cat',
                'state': self.test_city.state.code,
                'city': self.test_city.code,
                'kind': pet.kind.id,
                'status': pet.status.id,
                'profile_picture': pet.profile_picture.url
            }
        )
        response_get = self.client.get(pet.get_absolute_url())

        self.assertRedirects(response_post, pet.get_absolute_url())
        self.assertContains(response_get, 'Testing Fuzzy Boots')

    def test_show_facebook_link(self):
        """Displays a link to the Facebook profile of the owner in the of the pet's details"""
        pet = self.create_pet()

        resp_with_facebook = self.client.get(pet.get_absolute_url())

        self.assertContains(resp_with_facebook, 'http://www.facebook.com/owner_profile')

    def test_show_link_for_owner_profile(self):
        """Displays a link to the profile of the owner"""
        pet = self.create_pet()

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, reverse('users:user_profile', args=[self.admin.id]))

    def test_should_redirect_if_not_confirmed(self):
        """Don't allow users to register a pet if their info are not confirmed"""
        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('meupet:register'))

        self.assertRedirects(response, '/user/profile/edit/')

    def test_should_access_if_confirmed(self):
        """Allow user to access the pet register page if the information is confirmed"""
        self.admin.is_information_confirmed = True
        self.admin.save()
        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('meupet:register'))

        self.assertTemplateUsed(response, 'meupet/register_pet.html')

    def test_only_owner_can_see_edit_page(self):
        """Do not show the edit page if the logged user is not the owner"""
        OwnerProfile.objects.create_user(username='Other User', password='otherpass')
        pet = self.create_pet()
        self.client.login(username='Other User', password='otherpass')

        response = self.client.get(reverse('meupet:edit', args=[pet.slug]))

        self.assertRedirects(response, pet.get_absolute_url())

    def test_display_status_on_pet_page(self):
        """Show the name of the pet and the readable status name"""
        missing_pet = self.create_pet()

        response_missing = self.client.get(missing_pet.get_absolute_url())

        self.assertContains(response_missing, '{0} - {1}'.format(
            missing_pet.name,
            missing_pet.status.description,
        ))

    def test_incorrect_form_submission_reload_page_with_values(self):
        """Incomplete form submission should reload the page
        preserving the submitted information"""
        self.client.login(username='admin', password='admin')

        response = self.client.post(reverse('meupet:register'),
                                    {'description': 'Test Description'},
                                    follow=True)

        self.assertContains(response, 'Test Description')

    def test_show_add_photo_button_in_pet_page_owner_logged_in(self):
        """Display button to add more photos to the pet profile"""
        pet = self.create_pet()
        self.client.login(username='admin', password='admin')

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Submit Image')
        self.assertContains(response, 'another_picture')

    def test_show_city(self):
        """Display the name of the city where the pet belongs"""
        pet = self.create_pet(city=self.test_city)

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, self.test_city)

    def test_show_size(self):
        """Display the human readable size of the pet"""
        pet = self.create_pet(size=Pet.SMALL)

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Small')

    def test_search_without_filters(self):
        """Show message informing the user that she needs to use at least
        one filter to be able to search"""
        response = self.client.post(reverse('meupet:search'), {})

        self.assertContains(response, 'You must select at least one filter')

    def test_search_with_filter(self):
        """Search by city should show the pet"""
        pet = self.create_pet(city=self.test_city)
        inactive_pet = self.create_pet(city=self.test_city, active=False)

        response = self.client.post(reverse('meupet:search'), {'city': self.test_city.id}, follow=True)

        self.assertContains(response, pet.name)
        self.assertNotContains(response, inactive_pet.name)
        self.assertContains(response, pet.city)

    def test_show_pet_sex(self):
        """Display the human readable sex of the pet"""
        pet = self.create_pet(sex=Pet.FEMALE)

        response = self.client.get(pet.get_absolute_url())

        self.assertContains(response, 'Female')

    def test_get_pets_unpublished(self):
        """Manager method should return pets not published on Facebook yet"""
        pet = self.create_pet()
        self.create_pet(published=True, _quantity=3)

        pets = Pet.objects.get_unpublished_pets()

        self.assertIn(pet, pets)
        self.assertEqual(pets.count(), 1)


class PaginationListPetViewTest(MeuPetTestCase):
    def setUp(self):
        super(PaginationListPetViewTest, self).setUp()
        self.status_group = mommy.make(StatusGroup)
        self.status = mommy.make(PetStatus, group=self.status_group)
        self.pet = self.create_pet(kind='First Kind', status=self.status)

    def test_get_page_query_string(self):
        """Should return the page informed in the query string"""
        resp = self.client.get(
            reverse('meupet:pet_list', args=[self.status_group.slug, self.pet.kind.slug]),
            {'page': 1},
        )

        self.assertContains(resp, self.pet.name)

    def test_page_not_integer(self):
        """In case of a non-integer page, i.e, incorrent url, we should show the first page"""
        pets, _ = paginate_pets(Pet.objects.all(), 'page')

        self.assertEqual(1, len(pets))
        self.assertEqual('First Kind', pets[0].kind.kind)

    def test_empty_page(self):
        """If the user inform an empty page we should present the last page with data"""
        pets, _ = paginate_pets(Pet.objects.all(), 42)

        self.assertEqual(1, len(pets))
        self.assertEqual('First Kind', pets[0].kind.kind)
