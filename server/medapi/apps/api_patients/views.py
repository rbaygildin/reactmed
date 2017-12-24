from rest_framework import viewsets

from apps.api_patients.serializers import PatientSerializer
from apps.core.models import Patient


class PatientApiView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

