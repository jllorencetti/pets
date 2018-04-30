from django.test import TestCase
from model_mommy import mommy

from meupet.context_processors import pets_count, sidemenu
from meupet.models import Pet, StatusGroup, PetStatus, Kind


class ContextProcessorsTestCase(TestCase):
    def setUp(self):
        self.status_group = mommy.make(StatusGroup)
        status = mommy.make(PetStatus, group=self.status_group)
        mommy.make(Pet, kind__kind='Dog', status=status)
        mommy.make(Pet, kind__kind='Cat', active=False)

    def test_pets_count(self):
        context = pets_count({})

        self.assertEqual(2, context['pets_count'])

    def test_sidemenu_data(self):
        group_count = StatusGroup.objects.count()
        expected_data = {
            'name': self.status_group.name,
            'slug': self.status_group.slug,
            'menu_items': Kind.objects.count_pets((self.status_group.statuses.all())),
        }

        context = sidemenu({})
        menu_data = {}
        for data in context['sidemenu']:
            if data['name'] == self.status_group.name:
                menu_data = data

        self.assertEqual(len(context['sidemenu']), group_count)
        self.assertEqual(menu_data['name'], expected_data['name'])
        self.assertEqual(menu_data['slug'], expected_data['slug'])
        self.assertEqual(menu_data['menu_items'].first(), expected_data['menu_items'].first())
