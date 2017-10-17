from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    if request.user is not None and request.user.is_active:
        return redirect(reverse('patients:list'))
    return render(request, 'main/index.html', {})


def about_view(request):
    return render(request, 'main/about.html', {})


def help_view(request):
    return render(request, 'main/help.html', {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request=request, user=user)
                if user.is_superuser and user.role == 'ADMIN':
                    return redirect(reverse('admin:index'))
                return redirect(reverse('patients:list'))
    return redirect(reverse('main:index'))
