import json

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from cities.models import City, State


class CityViewTestCase(APITestCase):
    def setUp(self):
        self.state = State.objects.create(code=1, name='State', abbr='st')
        self.city = City.objects.create(code=1, name='City', search_name='city',
                                        state=self.state, lat=10.550975, lon=34.644608)

    def test_correct_fields_list(self):
        """Verify the correct serializer is being used"""
        response = self.client.get(reverse('api:city-list'))

        response_json = json.loads(response.content.decode('utf-8'))
        expected = [
            {
                'code': 1,
                'name': 'City',
                'search_name': 'city',
                'lat': 10.550975,
                'lon': 34.644608,
            },
        ]

        self.assertEqual(1, len(response_json['results']))
        self.assertEqual(expected, response_json['results'])

    def test_filter_city(self):
        """Should filter the cities based on the query parameters"""
        City.objects.create(code=2, name='New City', search_name='new city',
                            state=self.state, lat=40.730610, lon=-73.935242)
        response = self.client.get(reverse('api:city-list'), {'state': 1, 'city': 'new'})
        response_json = json.loads(response.content.decode('utf-8'))
        expected = [
            {
                'code': 2,
                'name': 'New City',
                'search_name': 'new city',
                'lat': 40.730610,
                'lon': -73.935242,
            }
        ]

        self.assertEqual(1, len(response_json['results']))
        self.assertEqual(expected, response_json['results'])
