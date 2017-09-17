from rest_framework.serializers import *

from apps.core.models import *
from apps.rest.models import Signup


class SignupSerializer(Serializer):

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


class MedAreaSerializer(ModelSerializer):
    class Meta:
        model = MedArea
        fields = ('id', 'name', 'description')
        ordering = ('name',)


class MedTestSerializer(ModelSerializer):
    class Meta:
        model = MedTest
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
    text_ind = ListField(child=CharField())

    class Meta:
        model = TextInd
        fields = ('id', 'name', 'description', 'values')
        ordering = ('name',)
