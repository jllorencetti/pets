from django.shortcuts import resolve_url
from django.test import TestCase

from meupet.models import Kind


class LostKindView(TestCase):
    def setUp(self):
        self.kind = Kind.objects.create(kind='Kind')

    def test_get_lost(self):
        resp = self.client.get(resolve_url('meupet:lost', self.kind.id))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')

    def test_get_lost_slug(self):
        resp = self.client.get(resolve_url('meupet:lost', self.kind.slug))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')

    def test_get_adoption(self):
        resp = self.client.get(resolve_url('meupet:adoption', self.kind.id))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')

    def test_get_adoption_slug(self):
        resp = self.client.get(resolve_url('meupet:adoption', self.kind.slug))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')

    def test_get_fallback(self):
        resp = self.client.get('/pets/lost/{}/'.format(self.kind.id))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')


class AdoptionKindView(TestCase):
    def setUp(self):
        self.kind = Kind.objects.create(kind='Kind')

    def test_get(self):
        resp = self.client.get(resolve_url('meupet:adoption', self.kind.id))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')

    def test_get_fallback(self):
        resp = self.client.get('/pets/adoption/{}/'.format(self.kind.id))

        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'meupet/pet_list.html')
