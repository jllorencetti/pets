from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from . import views

app_name = "users"
urlpatterns = [
    url(r"^$", views.CreateUserView.as_view(), name="create"),
    url(r"^profile/(?P<pk>[0-9]+)/$", views.ProfileDetailView.as_view(), name="user_profile"),
    url(r"^profile/$", views.UserProfileView.as_view(), name="profile"),
    url(r"^profile/edit/$", views.EditUserProfileView.as_view(), name="edit"),
    url(r"^login/$", views.UserLogin.as_view(), name="login"),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    url(r"^confirm/$", views.confirm_information, name="confirm_information"),
    url(r"^recover/$", views.RecoverView.as_view(), name="recover_password"),
    url(r"^recover/reset/done/$", views.RecoverResetDoneView.as_view(), name="recover_password_done"),
    url(r"^recover/reset/(?P<token>.+)/$", views.RecoverResetView.as_view(), name="recover_password_reset"),
    url(r"^recover/(?P<signature>.+)/$", views.RecoverDoneView.as_view(), name="recover_password_sent"),
]
