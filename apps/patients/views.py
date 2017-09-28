from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.core.models import Patient
from apps.patients.forms import PatientForm

User = get_user_model()


@login_required
def list_action(request):
    patients = request.user.patients.all()
    return render(request, 'list.html', {'patients': patients})


@login_required
def create_action(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            pass
        return redirect(reverse('patients:list'))
    else:
        return render(request, 'create.html', {})


@login_required
def show_action(request):
    return render(request, 'show.html', {})
