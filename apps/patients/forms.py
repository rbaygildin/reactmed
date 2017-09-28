from django.forms import ModelForm

from apps.core.models import Patient


class PatientForm(ModelForm):

    def __init__(self, request):
        super(PatientForm, self).__init__(data=request.POST)
        self.doctor = request.user

    def save(self, commit=True):
        return Patient.objects.create(
            name=self.cleaned_data['name'],
            surname=self.cleaned_data['surname'],
            patronymic=self.cleaned_data['patronymic'],
            gender=self.cleaned_data['gender'],
            birthday=self.cleaned_data['birthday'],
            omi_card=self.cleaned_data['omi_card'],
            doctor=self.doctor
        )

    class Meta:
        model = Patient
        fields = ('name', 'surname', 'patronymic', 'gender', 'birthday')

