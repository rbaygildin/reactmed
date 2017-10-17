from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.core.models import MedTest


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


@login_required
def med_tests_help(request):
    med_tests = MedTest.objects.all()
    return render(request, 'main/med_tests_help.html', {'med_tests': med_tests})


@login_required
def show_med_test_help(request, test_id):
    med_test = MedTest.objects.get(pk=test_id)
    return render(request, 'main/med_test_help.html', {'med_test': med_test})
