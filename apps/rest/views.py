from rest_framework.generics import *

from apps.rest.serializers import *


class MedAreaListView(ListCreateAPIView):
    queryset = MedArea.objects.all()
    serializer_class = MedAreaSerializer


class MedAreaView(RetrieveUpdateDestroyAPIView):
    queryset = MedArea.objects.all()
    serializer_class = MedAreaSerializer


class MedTestListView(ListCreateAPIView):
    queryset = MedTest.objects.all()
    serializer_class = MedTestSerializer


class MedTestView(RetrieveUpdateDestroyAPIView):
    queryset = MedTest.objects.all()
    serializer_class = MedTestSerializer


class RealIndListView(ListCreateAPIView):
    queryset = RealInd.objects.all()
    serializer_class = MedTestSerializer


class RealIndView(RetrieveUpdateDestroyAPIView):
    queryset = RealInd.objects.all()
    serializer_class = MedTestSerializer


class IntIndListView(ListCreateAPIView):
    queryset = IntInd.objects.all()
    serializer_class = MedTestSerializer


class IntIndView(RetrieveUpdateDestroyAPIView):
    queryset = IntInd.objects.all()
    serializer_class = MedTestSerializer


class TextIndListView(ListCreateAPIView):
    queryset = TextInd.objects.all()
    serializer_class = MedTestSerializer


class TextIndView(RetrieveUpdateDestroyAPIView):
    queryset = TextInd.objects.all()
    serializer_class = MedTestSerializer
