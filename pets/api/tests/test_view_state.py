import json

from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from cities.models import State


class StateViewTestCase(APITestCase):
    def test_correct_fields_list(self):
        """Verify the correct serializer is being used"""
        State.objects.create(code=1, name='State', abbr='st')
        response = self.client.get(reverse('api:state-list'))

        response_json = json.loads(response.content.decode('utf-8'))
        expected = [
            {
                'name': 'State',
                'abbr': 'st',
            },
        ]

        self.assertEqual(1, len(response_json['results']))
        self.assertEqual(expected, response_json['results'])
