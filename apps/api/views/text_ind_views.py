from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.core.models import TextInd
from apps.api.serializers import MedTestSerializer


class TextIndListView(ListCreateAPIView):
    queryset = TextInd.objects.all()
    serializer_class = MedTestSerializer


class TextIndView(RetrieveUpdateDestroyAPIView):
    queryset = TextInd.objects.all()
    serializer_class = MedTestSerializer
