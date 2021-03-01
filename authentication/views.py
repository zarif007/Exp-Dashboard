from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


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

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
