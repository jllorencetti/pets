from django.shortcuts import resolve_url
from django.test import TestCase
from model_mommy import mommy

from meupet.models import Kind, StatusGroup, Pet, PetStatus


class StatusGroupView(TestCase):
    def setUp(self):
        self.status_group = StatusGroup.objects.create(slug='test', name='Name')
        initial_status = mommy.make(PetStatus, final=False, group=self.status_group)
        final_status = mommy.make(PetStatus, final=True, group=self.status_group)
        self.kind = Kind.objects.create(kind='Kind')
        mommy.make(Pet, status=initial_status, kind=self.kind)
        mommy.make(Pet, status=final_status, kind=self.kind)

    def test_get_status_group_list(self):
        resp = self.client.get(resolve_url('meupet:pet_list', self.status_group.slug, self.kind.id))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')

    def test_list_all_pets(self):
        resp = self.client.get(resolve_url('meupet:pet_list', self.status_group.slug, self.kind.slug))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, len(resp.context['pets']))
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')
