from rest_framework.serializers import *

from apps.core.models import *
from apps.rest.models import Signup


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
        fields = ('id', 'name', 'surname', 'patronymic', 'username', 'password')
        ordering = ('name', 'surname', 'patronymic',)


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = ('gender', 'birthday', 'rh', 'blood_group')


class MedAreaSerializer(ModelSerializer):
    class Meta:
        model = MedArea
        fields = ('id', 'name', 'description')
        ordering = ('name',)


class RealIndSerializer(ModelSerializer):
    class Meta:
        model = RealInd
        fields = ('id', 'name', 'description', 'min_norm', 'max_norm')
        ordering = ('name',)


class IntIndSerializer(ModelSerializer):
    class Meta:
        model = IntInd
        fields = ('id', 'name', 'description', 'min_norm', 'max_norm')
        ordering = ('name',)


class TextIndSerializer(ModelSerializer):
    values = ListField(child=CharField())

    class Meta:
        model = TextInd
        fields = ('id', 'name', 'description', 'values')
        ordering = ('name',)


class MedTestSerializer(ModelSerializer):
    real_inds = SerializerMethodField('_get_real_inds')
    int_inds = SerializerMethodField('_get_int_inds')
    text_inds = SerializerMethodField('_get_text_inds')

    class Meta:
        model = MedTest
        fields = ('id', 'name', 'description', 'real_inds', 'int_inds', 'text_inds')
        ordering = ('name',)

    def _get_real_inds(self, obj):
        serializer = RealIndSerializer(obj.real_inds.all(), many=True)
        return serializer.data

    def _get_int_inds(self, obj):
        serializer = RealIndSerializer(obj.int_inds.all(), many=True)
        return serializer.data

    def _get_text_inds(self, obj):
        serializer = RealIndSerializer(obj.text_inds.all(), many=True)
        return serializer.data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.view_name = validated_data.get('view_name', instance.view_name)
        instance.description = validated_data.get('description', instance.description)
        return instance
