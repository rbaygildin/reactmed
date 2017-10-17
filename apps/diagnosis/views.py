from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.core.models import Diagnosis, Patient
from apps.diagnosis.forms import DiagnosisForm


@login_required
def show_action(request, diagnosis_id):
    diagnosis = Diagnosis.objects.get(pk=diagnosis_id)
    return render(request, 'diagnosis/show.html', {'diagnosis': diagnosis})


@login_required
def create_action(request, patient_id):
    if request.POST:
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('patients:patient_diagnosis', kwargs={'patient_id': patient_id}))
    patient = Patient.objects.get(pk=patient_id)
    return render(request, 'diagnosis/create.html', {'patient': patient})


@login_required
def delete_action(request, diagnosis_id):
    diagnosis = Diagnosis.objects.get(pk=diagnosis_id)
    patient_id = diagnosis.patient_id
    diagnosis.delete()
    return redirect(reverse('patients:patient_diagnosis', kwargs={'patient_id': patient_id}))
