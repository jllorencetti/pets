from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from meupet.models import Pet


class PetEntrySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Pet.objects.all()

    @staticmethod
    def lastmod(obj):
        return obj.modified


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return [
            'common:homepage',
            'common:about',
            'meupet:index',
            'meupet:search',
        ]

    def location(self, item):
        return reverse(item)
