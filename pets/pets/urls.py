from django.conf import settings
from django.conf.urls import include, url, static
from django.contrib import admin


urlpatterns = [
    url(r'^pets/', include('meupet.urls', namespace='meupet')),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^user/', include('users.urls', namespace='users')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('common.urls', namespace='common')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
