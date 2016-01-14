from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import django.contrib.auth.views as django_views

from . import models as pyschool_models

from . import challenges

def index(request):
    prog = None
    try:
        prog = pyschool_models.UserProgress.objects.get(user=request.user)
    except:
        if str(request.user) != 'AnonymousUser':
            print 'new progress object'
            prog = pyschool_models.UserProgress()
            prog.user = request.user
            prog.level = 1
            prog.completed = ""
            prog.save()

    return render(request, 'index.html',
        {
            'logged_in': str(request.user) != 'AnonymousUser',
            'set': challenges.get_challenges(prog.level) if prog else None
        })

def logout(request):
    django_views.logout(request)
    return HttpResponseRedirect('/')

def login(request):
    print 'through'
    try:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            print 'test'
            django_views.login(request)
            return HttpResponse()
    except Exception as e:
        print e
    return HttpResponse(status=403)

def register(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, password=password)

        prog = pyschool_models.UserProgress()
        prog.user = user
        prog.level = 1
        prog.completed = ""
        prog.save()

        django_views.login(request)
    except:
        pass
    return HttpResponse()

def get_challenge(request):
    pass
