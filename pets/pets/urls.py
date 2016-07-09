from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^pets/', include('meupet.urls', namespace='meupet')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^user/', include('users.urls', namespace='users')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('common.urls', namespace='common')),
)

handler404 = 'common.views.not_found'

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
