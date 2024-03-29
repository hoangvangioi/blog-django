from django.urls import path, re_path

from . import views
from .views import (
    DashboardHomeView,
    AuthorProfileUpdateView,
    AuthorProfileView,
)


urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    re_path(r"^register/(?P<key>[^/]+)/confirm$", views.user_register_confirm, name="register-confirm",),
    path("account/", views.user_account, name="account"),
    path("account/edit/", views.edit_profile, name="edit-profile"),
    re_path(r"^account/change-email/(?P<key>[^/]+)/confirm$", views.confirm_change_email, name="change-email-confirm",),
    path("account/password/", views.edit_password, name="edit-password"),
    path("account/cancel/", views.user_delete, name="delete"),
    re_path(r"^account/cancel/(?P<key>[^/]+)/confirm$", views.user_delete_confirm, name="delete-confirm",),

    # DASHBOARD URLS #

    # Author view profile home
    path('author/dashboard/home/', DashboardHomeView.as_view(), name="dashboard_home"),

    # Author view profile details
    path('author/profile/details/', AuthorProfileView.as_view(), name='author_profile_details'),

    # author update profile
    path('author/profile/update/', AuthorProfileUpdateView.as_view(), name='author_profile_update'),
]