from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from password_validator import PasswordValidator


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
        schema.min(8).max(100).has().uppercase().has().lowercase().has().digits()

        if not schema.validate(password):
            return JsonResponse({'password_error': 'not a valid password(At least 8 charecter, \
                                                    both upper and lower case, must contains digits)'}, 
                                status=400)

        
        return JsonResponse({'password_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
