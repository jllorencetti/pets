from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.PetIndexView.as_view(), name='index'),
    url(r'^novo/$', views.RegisterPetView.as_view(), name='register'),
    url(r'^desaparecidos/(?P<id>[0-9]+)/$', views.LostPetView.as_view(), name='lost'),
    url(r'^para-adocao/(?P<id>[0-9]+)/$', views.AdoptionPetView.as_view(), name='adoption'),
    url(r'^busca-rapida/$', views.QuickSearchView.as_view(), name='quick_search'),
    url(r'^busca/$', views.SearchView.as_view(), name='search'),
    url(r'^pet/(?P<slug>.+)/foto/$', views.upload_image, name='upload_image'),
    url(r'^(?P<slug>.+)/editar/$', views.EditPetView.as_view(), name='edit'),
    url(r'^(?P<slug>.+)/poster/$', views.poster, name='poster'),
    url(r'^(?P<slug>.+)/editar/situacao/$', views.change_status, name='change_status'),
    url(r'^(?P<slug>.+)/deletar/$', views.delete_pet, name='delete_pet'),
    url(r'^(?P<slug>.+)/registrado/$', views.registered, name='registered'),
    url(r'^(?P<pk_or_slug>.+)/$', views.pet_detail_view, name='detail'),

    # I'll keep this here for compatibility with links shared
    # on Facebook.
    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditPetView.as_view()),
    url(r'^(?P<pk>[0-9]+)/registered/$', views.registered),
    url(r'^(?P<pet_id>[0-9]+)/edit/status/$', views.change_status),
    url(r'^(?P<pet_id>[0-9]+)/delete/$', views.delete_pet),
    url(r'^new/$', views.RegisterPetView.as_view()),
    url(r'^lost/(?P<id>[0-9]+)/$', views.LostPetView.as_view()),
    url(r'^adoption/(?P<id>[0-9]+)/$', views.AdoptionPetView.as_view()),
    url(r'^quick-search/$', views.QuickSearchView.as_view()),
    url(r'^search/$', views.SearchView.as_view()),
    url(r'^pet/(?P<pet_id>[0-9]+)/photo/$', views.upload_image),
)
