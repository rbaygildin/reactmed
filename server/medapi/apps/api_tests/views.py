from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *

from apps.api.serializers import *
from apps.core.models import MedArea, MedTest, RealInd, TextInd, TestRec


class MedAreaApiViewSet(ModelViewSet):
    """
    Rest endpoint presents all registered medical areas (ex: oncology, cardiology)
    """
    serializer_class = MedAreaSerializer
    queryset = MedArea.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class RealIndApiViewSet(ModelViewSet):
    """
    Rest endpoint presents all registered real indicators
    """
    serializer_class = RealIndSerializer
    queryset = RealInd.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class TextIndApiViewSet(ModelViewSet):
    """
    Rest endpoint presents all registered text indicators
    """
    serializer_class = TextIndSerializer
    queryset = TextInd.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class MedTestApiViewSet(ModelViewSet):
    """
    Rest endpoint presents all registered medical tests
    """
    serializer_class = MedTestSerializer
    queryset = MedTest.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class TestRecApiViewSet(ModelViewSet):
    """
    Rest endpoint presents all saved test records for specific patients
    """
    serializer_class = TestRecSerializer
    queryset = TestRec.objects.all()
    permission_classes = [IsAuthenticated]
