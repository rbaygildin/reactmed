from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.core.models import IntInd
from apps.api.serializers import MedTestSerializer


class IntIndListView(ListCreateAPIView):
    queryset = IntInd.objects.all()
    serializer_class = MedTestSerializer


class IntIndView(RetrieveUpdateDestroyAPIView):
    queryset = IntInd.objects.all()
    serializer_class = MedTestSerializer
