from django.forms import ModelForm, ModelChoiceField

from apps.core.models import Diagnosis, Patient


class DiagnosisForm(ModelForm):
    patient = ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Diagnosis
        fields = (
            'diagnosis', 'diagnosis_date', 'diagnosis_type',
            'other_diseases', 'summary', 'complications',
            'info', 'patient'
        )
