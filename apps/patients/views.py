from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.core.models import Patient
from apps.patients.forms import PatientForm

User = get_user_model()


@login_required
def create_action(request):
    if request.method == 'POST':
        form = PatientForm(request)
        if form.is_valid():
            form.save()
        return redirect(reverse('patients:list'))
    else:
        return render(request, 'patients/create.html', {})


@login_required
def show_action(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    return render(request, 'patients/show.html', {
        'patient': patient
    })


@login_required
def update_action(request):
    patient_id = None
    if request.method == 'POST':
        patient_id = int(request.POST['patient_id'])
        form = PatientForm(request)
        if form.is_valid():
            form.update()
    return redirect(reverse('patients:show', kwargs={'patient_id': patient_id}))


@login_required
def delete_action(request, patient_id):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=patient_id)
        patient.delete()
        return HttpResponseRedirect(reverse('patients:list'))
    return redirect(reverse('patients:show', kwargs={'patient_id': patient_id}))
