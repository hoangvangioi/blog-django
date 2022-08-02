from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from .forms import PasswordChangeForm, SetPasswordForm

urlpatterns = [
    # Register, Login and Logout
    path('register/', views.SignUpView.as_view(), name='register'),
    # path('login/', views.LogInView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(
        template_name = 'accounts/login.html',
        next_page='post',
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
            template_name='registration/logged_out.html',
            next_page=None
        ),
        name = 'logout'),
    # Activate
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),

    # Change Password
    path('change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/change-password.html',
            success_url = '/',
            form_class = PasswordChangeForm,
        ),
        name='change_password'
    ),

    path('change-password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password-reset/password_reset_done.html'
        ),
        name='password_change_done'
    ),

    # Forget Password
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password-reset/password_reset.html',
            subject_template_name='accounts/password-reset/password_reset_subject.txt',
            email_template_name='accounts/password-reset/password_reset_email.html',
            success_url='/accounts/login/',
        ),
        name='password_reset'),

    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password-reset/password_reset_done.html'
        ),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password-reset/password_reset_confirm.html',
            form_class = SetPasswordForm,
        ),
        name='password_reset_confirm'),

    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password-reset/password_reset_complete.html'
        ),
        name='password_reset_complete'),

    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile'),

    path('edit-profile/<slug:slug>/', ProfileUpdateView.as_view(), name='edit_profile')
]