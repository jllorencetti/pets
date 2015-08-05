from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^sobre/$', views.AboutPageView.as_view(), name='about'),
    url(r'^associacoes/$', views.AssociacoesView.as_view(), name='associacoes'),
    url(r'^pet/(?P<id>[0-9]+)/$', views.PetDetailView.as_view(), name='detail'),
    url(r'^pet/(?P<pk>[0-9]+)/edit/$', views.EditPetView.as_view(), name='edit'),
    url(r'^pet/(?P<pet_id>[0-9]+)/edit/status/$', views.change_status, name='change_status'),
    url(r'^pet/lost/$', views.RegisterLostPetView.as_view(), name='register_lost'),
    url(r'^pet/adoption/$', views.RegisterAdoptionPetView.as_view(), name='register_adoption'),
    url(r'^lost/(?P<id>[0-9]+)/$', views.LostPetView.as_view(), name='lost'),
    url(r'^adoption/(?P<id>[0-9]+)/$', views.AdoptionPetView.as_view(), name='adoption'),
    url(r'^pet/(?P<pet_id>[0-9]+)/photo/$', views.upload_image, name='upload_image'),
    url(r'^quick-search/$', views.QuickSearchView.as_view(), name='quick_search'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
)
