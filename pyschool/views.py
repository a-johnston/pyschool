from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import django.contrib.auth.views as django_views
from django.views.decorators.csrf import ensure_csrf_cookie

from . import models as pyschool_models

from . import challenges


@ensure_csrf_cookie
def index(request):
    prog = None
    try:
        prog = pyschool_models.UserProgress.objects.get(user=request.user)
    except:
        if str(request.user) != 'AnonymousUser':
            print('new progress object')
            prog = pyschool_models.UserProgress()
            prog.user = request.user
            prog.level = 1
            prog.completed = ""
            prog.save()

    challengeset = None
    if prog:
        complete = prog.completed.split('|')
        print(complete)
        rawset = challenges.get_challenges(prog.level)
        challengeset = (
            rawset[0],
            map(lambda c: (c, c.name in complete), rawset[1]))

    return render(request, 'index.html',
                  {
                    'logged_in': str(request.user) != 'AnonymousUser',
                    'set': challengeset
                  })


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

        prog = pyschool_models.UserProgress()
        prog.user = user
        prog.level = 1
        prog.completed = ""
        prog.save()

        django_views.login(request)
    except:
        pass
    return HttpResponse()


def submit_challenge(request):
    try:
        if str(request.user) == 'AnonymousUser':
            return HttpResponse('failed')
        prog = None
        try:
            prog = pyschool_models.UserProgress.objects.get(user=request.user)
        except:
            return HttpResponse('failed')

        chal = challenges.lookup_challenge(prog.level, request.POST['name'])

        if chal.test(request.POST['code']):
            if chal.name not in prog.completed:
                prog.completed += chal.name + '|'
                if challenges.level_complete(prog.level, prog.completed):
                    prog.level = prog.level + 1
                    prog.save()
                    return HttpResponse('success complete')
                prog.save()
            return HttpResponse('success')
        else:
            return HttpResponse('failed')
    except Exception as e:
        print(e)
    return HttpResponse('failed')
