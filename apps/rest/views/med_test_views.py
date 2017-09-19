from rest_framework.generics import *

from apps.rest.serializers import *


class MedTestListView(ListCreateAPIView):
    queryset = MedTest.objects.all()
    serializer_class = MedTestSerializer


class MedTestView(RetrieveUpdateDestroyAPIView):
    queryset = MedTest.objects.all()
    serializer_class = MedTestSerializer