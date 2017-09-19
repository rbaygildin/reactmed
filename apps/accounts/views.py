from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.accounts.forms import SignUpForm


@login_required
def show_view(request):
    return render(request, 'account.html', {})


def create_account_view(request):
    if request.method == 'GET':
        return render(request, 'create_account.html', {})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.create_account()
            return redirect(reverse('index:index'))
        else:
            return redirect(reverse('accounts:create'))
    return redirect(reverse('index:index'))


def logout_view(request):
    logout(request)
    return redirect(reverse('index:index'))
