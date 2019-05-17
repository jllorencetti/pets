from django.test import TestCase

from cities import models


class CityQuerySetTest(TestCase):
    def setUp(self):
        state = models.State.objects.create(code=35, name="São Paulo", abbr="SP")
        models.City.objects.create(code=350330, state=state, name="Araras")

    def test_get_city(self):
        """Should be able to get city by it's name"""
        city = models.City.objects.get_city("Araras")
        expected = ["Araras"]
        self.assertQuerysetEqual(city, expected, lambda o: o.name)
