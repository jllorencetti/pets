from django.template import Template, Context
from django.test import TestCase

from model_mommy import mommy

from meupet.models import Pet, Kind


class TestTemplateTag(TestCase):
    def setUp(self):
        dog = Kind.objects.create(kind='Dog')
        cat = Kind.objects.create(kind='Cat')
        mommy.make(Pet, kind=dog, status=Pet.MISSING)
        mommy.make(Pet, kind=cat, status=Pet.FOR_ADOPTION)

    def test_render_menu(self):
        template = Template('{% load meupet_tags %}{% sidemenu %}')
        content = template.render(Context())

        self.assertIn('Dog <span class="badge">1</span></a>', content)
        self.assertIn('Cat <span class="badge">1</span></a>', content)
        self.assertIn('Missing', content)
        self.assertIn('For Adoption', content)
