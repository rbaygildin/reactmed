from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.appointments.forms import AppointmentForm
from apps.core.models import Appointment


@login_required
def create_action(request):
    if request.method == 'GET':
        return render(request, 'appointments/create.html', {})
    else:
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save_appointment(request.POST.get('patient_id'))
            return redirect(reverse('patients:appointments'))
    return render(request, 'appointments/create.html', {})


@login_required
def show_action(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    patient = appointment.patient
    return render(request, 'appointments/show.html', {'appointment': appointment, 'patient': patient})


@login_required
def finish_action(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.info = request.POST.get('info', None)
    appointment.complaints = request.POST.get('complaints', None)
    appointment.status = 'Завершено'
    appointment.save()
    return redirect(reverse('patients:appointments'))


@login_required
def cancel_action(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.status = 'Отменено'
    appointment.save()
    return redirect(reverse('patients:appointments'))
