from rest_framework.generics import *

from apps.api.serializers import *


class MedAreaListView(ListCreateAPIView):
    queryset = MedArea.objects.all()
    serializer_class = MedAreaSerializer


class MedAreaView(RetrieveUpdateDestroyAPIView):
    queryset = MedArea.objects.all()
    serializer_class = MedAreaSerializer
