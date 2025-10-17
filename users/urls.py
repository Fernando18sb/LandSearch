from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    register, logout_view, profile, verify_email,
    PasswordReset, PasswordResetConfirm,
    PasswordResetComplete, PasswordResetDone
)

urlpatterns = [
    path('register/', register, name='register'),
    path('accounts/login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('verify/<data>', verify_email, name='verify-email'),
    path(
        'password-reset/',
         PasswordReset.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'
    ),
    path(
        'password-reset-complete/',
         PasswordResetComplete.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirm.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'
    ),
    path(
        'password-reset/done/',
         PasswordResetDone.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'
    ),
]