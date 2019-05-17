import os
import tempfile

from django.conf import settings
from django.test import TestCase

from cities import models, utils

STATES_FILE = """code,abbr,name
12,AC,Acre
35,SP,São Paulo
"""

CITIES_FILE = """code,name,state
120001,Acrelândia,AC
350330,Araras,SP
"""


def save_content_to_tmp_file(content):
    filename = os.path.join(tempfile.mkdtemp(), "testing.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename


class UtilsTest(TestCase):
    def test_get_states_filename(self):
        """Should get the full path to the states data file"""
        directory = utils.get_states_filename("Brazil")
        expected = os.path.join(settings.CITIES_DATA_LOCATION, "brazil", "states.csv")
        self.assertEqual(directory, expected)

    def test_get_cities_filename(self):
        """Should get the full path to the cities data file"""
        directory = utils.get_cities_filename("Brazil")
        expected = os.path.join(settings.CITIES_DATA_LOCATION, "brazil", "cities.csv")
        self.assertEqual(directory, expected)

    def test_load_states(self):
        """Should load the correct states from the file"""
        filename = save_content_to_tmp_file(STATES_FILE)
        utils.load_states_from_file(filename)

        acre = models.State.objects.get(code=12)
        sao_paulo = models.State.objects.get(code=35)

        self.assertEqual("AC", acre.abbr)
        self.assertEqual("Acre", acre.name)

        self.assertEqual("SP", sao_paulo.abbr)
        self.assertEqual("São Paulo", sao_paulo.name)

    def test_load_cities(self):
        """Should load the correct cities from the file"""
        states_file = save_content_to_tmp_file(STATES_FILE)
        cities_file = save_content_to_tmp_file(CITIES_FILE)
        utils.load_states_from_file(states_file)
        utils.load_cities_from_file(cities_file)

        acrelandia = models.City.objects.get(code=120001)
        araras = models.City.objects.get(code=350330)

        self.assertEqual("AC", acrelandia.state.abbr)
        self.assertEqual("Acrelândia", acrelandia.name)
        self.assertEqual("acrelandia", acrelandia.search_name)

        self.assertEqual("SP", araras.state.abbr)
        self.assertEqual("Araras", araras.name)
        self.assertEqual("araras", araras.search_name)
