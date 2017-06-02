from django.test import TestCase

from cities.models import State
from api.serializers import StateSerializer


class StateSerializerTestCase(TestCase):
    def test_assert_correct_fields(self):
        """The serializer should include only the name and abbr fields"""
        sp = State(name='São Paulo', abbr='SP')
        serializer_data = StateSerializer(sp).data

        self.assertEqual(2, len(serializer_data))
        self.assertEqual('São Paulo', serializer_data['name'])
        self.assertEqual('SP', serializer_data['abbr'])
