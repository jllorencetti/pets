from json import loads

from django.shortcuts import resolve_url
from django.test import TestCase
from meupet.models import City, Kind, Pet
from users.models import OwnerProfile


class TestGetHome(TestCase):

    def setUp(self):
        City.objects.create(city='Araras')

        OwnerProfile.objects.create_user(
            'johndoe',
            'john@doe.cc',
            'secret',
            first_name='John',
            last_name='Doe',
            facebook='https://fb.com/4',
        )

        published_pet_data = {
            'owner': OwnerProfile.objects.first(),
            'name': 'Costela',
            'description': 'Costelinha',
            'city': City.objects.first(),
            'kind': Kind.objects.first(),
            'status': Pet.FOR_ADOPTION,
            'size': Pet.SMALL,
            'sex': Pet.MALE,
            'published': True,
        }
        Pet.objects.create(**published_pet_data)

        self.resp = self.client.get(resolve_url('api:home'))
        self.json = loads(self.resp.content.decode())

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        pet = self.json[0]
        pet_profile = resolve_url('meupet:detail', 1)
        user_profile = resolve_url('users:user_profile', 1)

        with self.subTest():
            self.assertEqual(1, len(self.json))
            self.assertIn(pet_profile, pet['id'])
            self.assertIn(user_profile, pet['owner']['id'])
            self.assertEqual('John Doe', pet['owner']['name'])
            self.assertEqual('https://fb.com/4', pet['owner']['facebook'])
            self.assertEqual('Costela', pet['name'])
            self.assertEqual('Costelinha', pet['description'])
            self.assertEqual('Araras', pet['city'])
            self.assertEqual('Gato', pet['kind'])
            self.assertEqual('Para Adoção', pet['status'])
            self.assertEqual('Pequeno', pet['size'])
            self.assertEqual('Macho', pet['sex'])


class TestPostHome(TestCase):

    def setUp(self):
        super().setUp()
        self.resp = self.client.post(resolve_url('api:home'))

    def test_post(self):
        self.assertEqual(405, self.resp.status_code)
