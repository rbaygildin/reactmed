from rest_framework.serializers import *
from apps.core.models import *


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
