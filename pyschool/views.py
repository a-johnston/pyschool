from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import django.contrib.auth.views as django_views
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'loggedIn': str(request.user) != 'AnonymousUser'})

def logout(request):
    django_views.logout(request)
    return HttpResponseRedirect('/')

def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            django_views.login(request)
            return HttpResponse()
    except:
        pass
    return HttpResponse(status=403)

def register(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, password=password)
        django_views.login(request)
    except:
        pass
    return HttpResponse()

def get_challenge(request):
    pass
