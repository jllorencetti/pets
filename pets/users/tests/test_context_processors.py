from django.test import TestCase
from model_mommy import mommy

from users.context_processors import users_count
from users.models import OwnerProfile


class ContextProcessors(TestCase):
    def setUp(self):
        mommy.make(OwnerProfile)

    def test_users_count(self):
        context = users_count({})

        self.assertEqual(1, context['users_count'])
