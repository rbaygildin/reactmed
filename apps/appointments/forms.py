from django.forms import ModelForm

from apps.core.models import Appointment, Patient


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('appointment_date', 'info')

    def save_appointment(self, patient_id):
        instance = super(AppointmentForm, self).save(commit=False)
        instance.patient = Patient.objects.get(pk=patient_id)
        instance.save()
        return instance
