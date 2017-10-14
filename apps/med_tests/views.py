from json import loads

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django_pdfkit import PDFView
from pdfkit import from_string

from apps.core.models import Patient, TestRec


@login_required
@csrf_exempt
def create_action(request, patient_id):
    if request.method == 'GET':
        return render(request, 'med_tests/create.html', {'patient_id': patient_id})
    elif request.method == 'POST':
        patient = Patient.objects.get(pk=patient_id)
        d = loads(request.body)
        TestRec.objects.create(
            name=d.get('name'),
            short_name=d.get('short_name'),
            description=d.get('description', None),
            real_inds=d.get('real_inds', None),
            int_inds=d.get('int_inds', None),
            text_inds=d.get('text_inds', None),
            info=d.get('info'),
            summary=d.get('summary'),
            test_date=d.get('test_date'),
            patient=patient
        )
    return redirect(reverse('patients:show', kwargs={'patient_id': patient_id}))


@login_required
def show_action(request, test_id):
    test_rec = TestRec.objects.get(pk=test_id)

    patient = test_rec.patient
    return render(
        request,
        'med_tests/show.html',
        {
            'test_rec': test_rec,
            'patient': patient
        }
    )


@login_required
def delete_action(request, test_id):
    test_rec = TestRec.objects.get(pk=test_id)
    test_rec.delete()
    return redirect(reverse('patients:list'))


@login_required
def dynamics_action(request, patient_id=None):
    return render(
        request,
        'med_tests/dynamics.html',
        {
            'patient': Patient.objects.get(pk=patient_id)
        }
    )
