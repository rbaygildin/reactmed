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
        fields = ('id', 'name', 'surname', 'patronymic', 'username', 'password')
        ordering = ('name', 'surname', 'patronymic',)
