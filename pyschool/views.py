from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {'loggedIn': str(request.user) != 'AnonymousUser'})

def login(request): 
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {
        'form': form,
    })

def logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def post_test(request):
    if request.method == 'POST':
        return HttpResponse(str(request.POST))
    else:
        return HttpResponse('yes')
