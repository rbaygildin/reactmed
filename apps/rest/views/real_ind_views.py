from rest_framework.generics import *

from apps.rest.serializers import *


class RealIndListView(ListCreateAPIView):
    queryset = RealInd.objects.all()
    serializer_class = MedTestSerializer


class RealIndView(RetrieveUpdateDestroyAPIView):
    queryset = RealInd.objects.all()
    serializer_class = MedTestSerializer
