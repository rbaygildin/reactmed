from rest_framework.serializers import ModelSerializer

from apps.core.models import Patient


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'surname', 'patronymic',
                  'gender', 'birthday', 'omi_card', 'short_info')
