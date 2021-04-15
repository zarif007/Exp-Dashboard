import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   force_text)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from password_validator import PasswordValidator
from validate_email import validate_email
from .utils import token_generator


class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should contain only alphanumeric characters'}, 
                                status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username is taken, chose another one'}, 
                                status=400)
        
        return JsonResponse({'username_valid': True})


class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'not a valid email address'}, 
                                status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email in use, You can log in with this email'}, 
                                status=400)
        
        return JsonResponse({'email_valid': True})


class PasswordValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']

        schema = PasswordValidator()
        schema.min(8).max(100).has().digits()

        if not schema.validate(password):
            return JsonResponse({'password_error': 'not a valid password(At least 8 charecter, \
                                                    both upper and lower case, must contains digits)'}, 
                                status=400)

        
        return JsonResponse({'password_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm_password']
        context = {
            'fieldvalues' : request.POST
        }

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        domain = get_current_site(request).domain
        link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

        email_subject = 'Activate your account'

        activating_url = f'http://{domain + link}'

        email_body = f'Hi {username} \n Click this link to activate your account \n {activating_url}'

        email = EmailMessage(
            email_subject,
            email_body,
            'zarifhuq007@gmail.com',
            [email],
        )

        email.send(fail_silently=False)

        messages.success(request, 'Acoount created Successfully!!')

        return render(request, 'authentication/register.html', context)


class VerificationView(View):

    def get(self, request, uidb4, token):
        return redirect('login')
