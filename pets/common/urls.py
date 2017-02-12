from django.conf.urls import patterns, url
from django.contrib.sitemaps.views import sitemap

from .sitemaps import PetEntrySitemap, PageSitemap
from . import views

sitemaps = {
    'pages': PageSitemap,
    'pets': PetEntrySitemap,
}

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='homepage'),
    url(r'^sobre/$', views.AboutPageView.as_view(), name='about'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
)
