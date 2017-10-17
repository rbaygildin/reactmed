from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.core.models import Patient, TestRec, Appointment, Diagnosis
from apps.patients.forms import PatientForm

User = get_user_model()


@login_required
def list_action(request):
    patients = request.user.patients.all()
    return render(
        request,
        'patients/list.html',
        {
            'patients': patients,
            'patients_count': patients.count
        }
    )


@login_required
def tests_action(request):
    patients_count = request.user.patients.count()
    tests = TestRec.objects.filter(patient__doctor_id=request.user.id)
    return render(
        request,
        'patients/tests.html',
        {
            'patients_count': patients_count,
            'tests': tests
        }
    )


@login_required
def patient_test_action(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    tests = patient.test_recs
    return render(
        request,
        'patients/patient_tests.html',
        {
            'patient': patient,
            'tests': tests
        }
    )


@login_required
def patient_dynamics_action(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    tests = patient.test_recs
    return render(
        request,
        'patients/patient_dynamics.html',
        {
            'patient': patient,
            'tests': tests
        }
    )


@login_required
def appointments_action(request):
    patients_count = request.user.patients.count()
    appointments = Appointment.objects.filter(patient__doctor_id=request.user.id)
    return render(
        request,
        'patients/appointments.html',
        {
            'patients_count': patients_count,
            'appointments': appointments
        }
    )


@login_required
def patient_appointments_action(request, patient_id):
    patients_count = request.user.patients.count()
    patient = Patient.objects.get(pk=patient_id)
    return render(
        request,
        'patients/patient_appointments.html',
        {
            'patients_count': patients_count,
            'patient': patient
        }
    )


@login_required
def patient_diagnosis_action(request, patient_id):
    patients_count = request.user.patients.count()
    patient = Patient.objects.get(pk=patient_id)
    return render(
        request,
        'patients/patient_diagnosis.html',
        {
            'patients_count': patients_count,
            'patient': patient
        }
    )


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
