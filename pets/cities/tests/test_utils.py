import os

from django.conf import settings
from django.test import TestCase

from cities import utils


class UtilsTest(TestCase):
    def test_get_states_filename(self):
        directory = utils.get_states_filename('Brazil')
        expected = os.path.join(settings.CITIES_DATA_LOCATION, 'brazil', 'states.csv')
        self.assertEqual(directory, expected)

    def test_get_cities_filename(self):
        directory = utils.get_cities_filename('Brazil')
        expected = os.path.join(settings.CITIES_DATA_LOCATION, 'brazil', 'cities.csv')
        self.assertEqual(directory, expected)
