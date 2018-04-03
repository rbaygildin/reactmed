from rest_framework.serializers import *

from apps.core.models import *
from apps.api.models import Signup


class SignupSerializer(Serializer):
    def is_valid(self, raise_exception=False):
        return True

    def create(self, validated_data):
        return Signup(**validated_data)

    def update(self, instance, validated_data):
        return instance

    name = CharField(max_length=70)
    surname = CharField(max_length=70)
    patronymic = CharField(max_length=70)
    username = CharField(max_length=70)
    password = CharField(max_length=70)
    confirm_password = CharField(max_length=70)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'patronymic', 'email', 'password')
        ordering = ('name', 'surname', 'patronymic',)


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'name', 'surname', 'patronymic', 'gender', 'birthday', 'omi_card', 'short_info')


class MedAreaSerializer(ModelSerializer):
    class Meta:
        model = MedArea
        fields = ('id', 'name', 'short_name', 'description')
        ordering = ('name',)


class RealIndSerializer(ModelSerializer):
    class Meta:
        model = RealInd
        fields = ('id', 'name', 'short_name', 'description', 'min_norm', 'max_norm', 'unit')
        ordering = ('name',)


class IntIndSerializer(ModelSerializer):
    class Meta:
        model = IntInd
        fields = ('id', 'name', 'short_name', 'description', 'min_norm', 'max_norm', 'unit')
        ordering = ('name',)


class TextIndSerializer(ModelSerializer):
    values = ListField(child=CharField(max_length=120), default=[])

    class Meta:
        model = TextInd
        fields = ('id', 'name', 'short_name', 'description', 'values')
        ordering = ('name',)


class MedTestSerializer(ModelSerializer):
    real_inds = SerializerMethodField('_get_real_inds')
    int_inds = SerializerMethodField('_get_int_inds')
    text_inds = SerializerMethodField('_get_text_inds')

    class Meta:
        model = MedTest
        fields = ('id', 'name', 'short_name', 'description', 'real_inds', 'int_inds', 'text_inds')
        ordering = ('name',)

    def _get_real_inds(self, obj):
        serializer = RealIndSerializer(obj.real_inds.all(), many=True)
        return serializer.data

    def _get_int_inds(self, obj):
        serializer = IntIndSerializer(obj.int_inds.all(), many=True)
        return serializer.data

    def _get_text_inds(self, obj):
        serializer = TextIndSerializer(obj.text_inds.all(), many=True)
        return serializer.data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        return instance


class TestRecSerializer(ModelSerializer):
    class Meta:
        model = TestRec
        fields = (
            'id', 'name', 'short_name', 'summary',
            'info', 'test_date', 'real_inds',
            'int_inds', 'text_inds'
        )
        ordering = ('test_date',)


class AttachmentSerializer(ModelSerializer):
    class Meta:
        model = Attachment
        fields = (
            'id', 'name', 'description', 'attachment_file'
        )


class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'id', 'appointment_date', 'info', 'complaints', 'status'
        )


class TreatmentSerializer(ModelSerializer):
    class Meta:
        model = Treatment
        fields = (
            'id', 'start_date', 'finish_date', 'summary', 'info'
        )


class MedicationSerializer(ModelSerializer):
    class Meta:
        model = Medication
        fields = (
            'id', 'summary', 'info', 'drugs', 'medication_date'
        )


class DiagnosisSerializer(ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = (
            'id', 'diagnosis', 'diagnosis_type', 'other_diseases', 'summary',
            'info', 'complications', 'diagnosis_date'
        )
