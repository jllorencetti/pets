from django.test import TestCase, override_settings

from common import context_processors, utils


class UtilsTest(TestCase):
    def test_clear_text(self):
        """Should remove combining marks from text"""
        sp = utils.clear_text('São Paulo')
        rand = utils.clear_text('ç~ã`é´â^ô')

        self.assertEqual('Sao Paulo', sp)
        self.assertEqual('caeao', rand)


@override_settings(
    GOOGLE_API_KEY='UA-12345678-9',
    HOTJAR_TRACKING_KEY='123456',
)
class ContextProcessor(TestCase):
    def test_context_processors_analytics(self):
        keys = context_processors.analytics({})

        self.assertEqual('UA-12345678-9', keys['GOOGLE_API_KEY'])
        self.assertEqual('123456', keys['HOTJAR_TRACKING_KEY'])
