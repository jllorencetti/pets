from model_mommy import mommy

from django.test import RequestFactory, TestCase

from api.serializers import PetSerializer
from meupet.models import Pet, PetStatus


class CitySerializerTestCase(TestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    def test_assert_correct_fields(self):
        """
        The serializer should contain pet fields
        """
        request = self.req_factory.get('/pet/api/')
        pet = mommy.make(Pet, status=mommy.make(PetStatus))
        serializer = PetSerializer(pet, context={'request': request})

        self.assertEqual(11, len(serializer.data))
