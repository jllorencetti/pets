from django.test import TestCase

from common import utils


class UtilsTest(TestCase):
    def test_clear_text(self):
        """Should remove combining marks from text"""
        sp = utils.clear_text('São Paulo')
        rand = utils.clear_text('ç~ã`é´â^ô')

        self.assertEqual('Sao Paulo', sp)
        self.assertEqual('caeao', rand)
