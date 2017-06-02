from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^pets/$', views.ListPets.as_view(), name='list_pets'),
    url(r'^states/$', views.StateList.as_view(), name='state-list'),
]
