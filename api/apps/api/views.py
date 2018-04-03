from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import *
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import *
from apps.api.serializers import *


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def check_login(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return JsonResponse(data={'error': 'Пользователь с таким логином не существует!'})
        if not user.check_password(password):
            return JsonResponse(data={'error': 'Пароль введен неправильно!'})
    return JsonResponse(data={})


class IntIndListView(ListCreateAPIView):
    queryset = IntInd.objects.all()
    serializer_class = MedTestSerializer


class IntIndView(RetrieveUpdateDestroyAPIView):
    queryset = IntInd.objects.all()
    serializer_class = MedTestSerializer


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


class PatientListView(ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        doctor = self.request.user
        return doctor.patients


class PatientView(ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class RealIndListView(ListCreateAPIView):
    queryset = RealInd.objects.all()
    serializer_class = MedTestSerializer


class RealIndView(RetrieveUpdateDestroyAPIView):
    queryset = RealInd.objects.all()
    serializer_class = MedTestSerializer


class SignupView(APIView):

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestRecListView(ListAPIView):
    serializer_class = TestRecSerializer

    def get_queryset(self):
        """
        This view should return a list of
        test records for specific patient
        during specific time period
        """
        patient_id = self.kwargs.get('patient_id')
        test_type = self.kwargs.get('test_type_id')
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date is None and end_date is None:
            return TestRec.objects.filter(patient__id=patient_id, short_name=test_type)
        elif start_date is not None and end_date is None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            return TestRec.objects.filter(patient__id=patient_id, short_name=test_type, test_date__gte=start_date)
        elif start_date is None and end_date is not None:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            return TestRec.objects.filter(patient__id=patient_id, short_name=test_type, test_date__lte=end_date)
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        return TestRec.objects.filter(patient__id=patient_id, short_name=test_type, test_date__gte=start_date,
                                      test_date__lte=end_date)


class TextIndListView(ListCreateAPIView):
    queryset = TextInd.objects.all()
    serializer_class = MedTestSerializer


class TextIndView(RetrieveUpdateDestroyAPIView):
    queryset = TextInd.objects.all()
    serializer_class = MedTestSerializer
