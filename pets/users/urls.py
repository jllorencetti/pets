from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.CreateUserView.as_view(), name='create'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileDetailView.as_view(), name='user_profile'),
    url(r'^profile/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^profile/edit/$', views.EditUserProfileView.as_view(), name='edit'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^confirm/$', views.confirm_information, name='confirm_information'),
    url(r'^recover/$', views.RecoverView.as_view(), name='recover_password'),
    url(r'^recover/reset/done/$', views.RecoverResetDoneView.as_view(), name='recover_password_done'),
    url(r'^recover/reset/(?P<token>.+)/$', views.RecoverResetView.as_view(), name='recover_password_reset'),
    url(r'^recover/(?P<signature>.+)/$', views.RecoverDoneView.as_view(), name='recover_password_sent'),
)
