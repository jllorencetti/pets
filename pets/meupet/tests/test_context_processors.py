from django.test import TestCase
from model_mommy import mommy

from meupet.context_processors import pets_count, kinds_count
from meupet.models import Pet


class ContextProcessorsTestCase(TestCase):
    def setUp(self):
        mommy.make(Pet, kind__kind='Dog', status=Pet.ADOPTED)
        mommy.make(Pet, active=False)

    def test_pets_count(self):
        context = pets_count({})

        self.assertEqual(2, context['pets_count'])

    def test_kind_count(self):
        context = kinds_count({})

        adoption_count = context['kind_adoption'].first().num_pets

        self.assertIn('kind_lost', context)
        self.assertIn('kind_adoption', context)
        self.assertEqual(adoption_count, 1)
