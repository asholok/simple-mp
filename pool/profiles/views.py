from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect

def login_user(request):
    logout(request)
    if request.POST:
        password = request.POST['password']
        username = request.POST['username']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
# Create your views here.
