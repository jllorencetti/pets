from django.test import TestCase

from api.serializers import CitySerializer
from cities.models import City


class CitySerializerTestCase(TestCase):
    def test_assert_correct_fields(self):
        """
        The serializer should include only the name and search_name fields
        """
        araras = City(code=1, name='Araras', search_name='araras')
        serializer_data = CitySerializer(araras).data

        self.assertEqual(5, len(serializer_data))
        self.assertEqual('Araras', serializer_data['name'])
        self.assertEqual('araras', serializer_data['search_name'])
        self.assertEqual(1, serializer_data['code'])
