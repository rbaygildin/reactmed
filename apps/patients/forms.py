from django.forms import ModelForm

from apps.core.models import Patient


class PatientForm(ModelForm):
    def __init__(self, request):
        super(PatientForm, self).__init__(data=request.POST)
        self.doctor = request.user
        self.request = request

    def save(self, commit=True):
        return Patient.objects.create(
            name=self.cleaned_data['name'],
            surname=self.cleaned_data['surname'],
            patronymic=self.cleaned_data['patronymic'],
            gender=self.cleaned_data['gender'],
            birthday=self.cleaned_data['birthday'],
            omi_card=self.cleaned_data['omi_card'],
            address=self.cleaned_data['address'],
            occupation=self.cleaned_data['occupation'],
            blood_group=self.cleaned_data['blood_group'],
            rh_factor=self.cleaned_data['rh_factor'],
            doctor=self.doctor
        )

    def update(self):
        patient = Patient.objects.get(pk=self.request.POST['patient_id'])
        patient.name = self.cleaned_data['name']
        patient.surname = self.cleaned_data['surname']
        patient.patronymic = self.cleaned_data['patronymic']
        patient.gender = self.cleaned_data['gender']
        patient.birthday = self.cleaned_data['birthday']
        patient.omi_card = self.cleaned_data['omi_card']
        patient.address = self.cleaned_data['address']
        patient.blood_group = self.cleaned_data['blood_group']
        patient.rh_factor = self.cleaned_data['rh_factor']
        patient.save()

    class Meta:
        model = Patient
        fields = ('name', 'surname', 'patronymic',
                  'gender', 'birthday', 'omi_card',
                  'address', 'occupation', 'blood_group', 'rh_factor')
