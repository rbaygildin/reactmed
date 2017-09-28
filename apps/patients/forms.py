from django.forms import ModelForm


class PatientForm(ModelForm):
    class Meta:
        fields = ('name', 'surname', 'patronymic', 'gender')

