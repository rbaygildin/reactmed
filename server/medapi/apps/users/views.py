from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.users.forms import SignUpForm, ChangePasswordForm, UpdateUserForm


def create_action(request):
    if request.method == 'GET':
        return render(request, 'users/create.html', {})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.create_account()
            return redirect(reverse('main:index'))
        else:
            return redirect(reverse('users:create'))
    return redirect(reverse('main:index'))


@login_required
def show_action(request):
    return render(request, 'users/show.html', {})


@login_required
def update_action(request):
    form = UpdateUserForm(request=request)
    if form.is_valid():
        form.update()
    return redirect(reverse('users:show'))


@login_required
def change_password_action(request):
    if request.method == 'POST':
        user = request.user
        form = ChangePasswordForm(request.POST, user=user)
        if form.is_valid():
            form.change_password(request=request)
    return redirect(reverse('users:show'))


def reset_password_action(request):
    pass


@login_required
def delete_action(request):
    if request.method == 'POST':
        password = request.POST['current_password']
        user = request.user
        if user.check_password(password):
            user.delete()
            logout(request)
            return redirect(reverse('main:index'))
    return redirect(reverse('users:show'))


@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('main:index'))


@login_required()
def dashboard_action(request):
    patients = request.user.patients.all()
    return render(request, 'users/dashboard.html', {'patients': patients})
