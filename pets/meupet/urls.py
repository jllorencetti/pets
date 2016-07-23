from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    # I'll keep this here for compatibility with links shared
    # on Facebook.
    url(r'^new/$', views.RegisterPetView.as_view()),
    url(r'^search/$', views.SearchView.as_view()),
    url(r'^lost/(?P<kind>[0-9]+)/$', views.lost_pets),
    url(r'^adoption/(?P<kind>[0-9]+)/$', views.adoption_pets),

    url(r'^$', views.PetIndexView.as_view(), name='index'),
    url(r'^novo/$', views.RegisterPetView.as_view(), name='register'),
    url(r'^desaparecidos/(?P<kind>[-\w]*)/$', views.lost_pets, name='lost'),
    url(r'^para-adocao/(?P<kind>[-\w]*)/$', views.adoption_pets, name='adoption'),
    url(r'^busca/$', views.SearchView.as_view(), name='search'),
    url(r'^pet/(?P<slug>[-\w]*)/foto/$', views.upload_image, name='upload_image'),
    url(r'^(?P<slug>[-\w]*)/editar/$', views.EditPetView.as_view(), name='edit'),
    url(r'^(?P<slug>[-\w]*)/poster/$', views.poster, name='poster'),
    url(r'^(?P<slug>[-\w]*)/editar/situacao/$', views.change_status, name='change_status'),
    url(r'^(?P<slug>[-\w]*)/deletar/$', views.delete_pet, name='delete_pet'),
    url(r'^(?P<slug>[-\w]*)/registrado/$', views.registered, name='registered'),

    url(r'^(?P<pk_or_slug>[-\w]*)/$', views.pet_detail_view, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.pet_detail_view, name='detail_by_pk'),
)
