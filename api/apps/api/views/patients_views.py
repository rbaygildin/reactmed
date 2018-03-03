from rest_framework.generics import ListAPIView

from apps.api.serializers import PatientSerializer


class PatientListView(ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        doctor = self.request.user
        return doctor.patients
