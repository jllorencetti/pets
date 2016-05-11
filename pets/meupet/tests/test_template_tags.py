from django.template import Template, Context
from django.test import TestCase

from meupet.models import Pet, Kind
from users.models import OwnerProfile


class TestTemplateTag(TestCase):
    def setUp(self):
        user = OwnerProfile.objects.create(username='user', password='user')
        dog = Kind.objects.create(kind='Dog')
        cat = Kind.objects.create(kind='Cat')
        Pet.objects.create(name='Testing', owner=user, kind=dog, status=Pet.MISSING)
        Pet.objects.create(name='Testing', owner=user, kind=cat, status=Pet.FOR_ADOPTION)

    def test_render_menu(self):
        template = Template('{% load meupet_tags %}{% sidemenu %}')
        content = template.render(Context())

        self.assertIn('Dog <span class="badge">1</span></a>', content)
        self.assertIn('Cat <span class="badge">1</span></a>', content)
        self.assertIn('Desaparecidos', content)
        self.assertIn('Para Adoção', content)
