from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    return render(request, 'main/index.html', {})


def about_view(request):
    return render(request, 'main/about.html', {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request=request, user=user)
                return redirect(reverse('patients:list'))
    return redirect(reverse('main:index'))
