from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import RegistrationView, UsernameValidation, EmailValidation, \
    PasswordValidation, VerificationView, LoginView, LogoutView

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidation.as_view()), 
                                name='validate_username'),
    path('validate-email', csrf_exempt(EmailValidation.as_view()), 
                                name='validate_email'),
    path('validate-password', csrf_exempt(PasswordValidation.as_view()), 
                                name='validate_password'),
    path('active/<uidb64>/<token>', csrf_exempt(VerificationView.as_view()), 
                                name='activate'),
]
