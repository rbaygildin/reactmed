from rest_framework.generics import ListAPIView

from apps.core.models import TestRec
from apps.rest.serializers import TestRecSerializer
from datetime import datetime


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
