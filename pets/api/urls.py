from django.conf.urls import url

from api.views import ListPets

urlpatterns = [
    url(r'^pets/$', ListPets.as_view(), name='list_pets'),
]
