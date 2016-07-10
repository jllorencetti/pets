from django.conf.urls import url
from api.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
]
