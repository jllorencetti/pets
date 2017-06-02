import json

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from cities.models import City, State


class CityViewTestCase(APITestCase):
    def test_correct_fields_list(self):
        """Verify the correct serializer is being used"""
        st = State.objects.create(code=1, name='State', abbr='st')
        City.objects.create(code=1, name='City', search_name='city', state=st)
        response = self.client.get(reverse('api:city-list'))

        response_json = json.loads(response.content.decode('utf-8'))
        expected = [
            {
                'name': 'City',
                'search_name': 'city',
            },
        ]

        self.assertEqual(1, len(response_json['results']))
        self.assertEqual(expected, response_json['results'])
