from apps.core.handlers import *
from apps.api.serializers import *
from apps.core.models import *


# Users
class UserListHandler(ListCreateHandler):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginHandler(CreateHandlerMixin):
    pass


class UserLogoutHandler(CreateHandlerMixin):
    pass


# Patients
class PatientListHandler(ListCreateHandler):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


# Med Areas
class MedAreaListHandler(ListCreateHandler):
    queryset = MedArea.objects.all()
    serializer_class = MedAreaSerializer


class MedAreaDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = MedArea.objects.all()
    serializer_class = MedAreaSerializer


# Med Tests
class MedTestListHandler(ListCreateHandler):
    queryset = MedTest.objects.all()
    serializer_class = MedTestSerializer


class MedTestDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = MedTest.objects.all()
    serializer_class = MedTestSerializer


# Real Inds
class RealIndListHandler(ListHandler):
    queryset = RealInd.objects.all()
    serializer_class = RealIndSerializer


class RealIndDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = RealInd.objects.all()
    serializer_class = RealIndSerializer


# Int Inds
class IntIndListHandler(ListHandler):
    queryset = IntInd.objects.all()
    serializer_class = IntIndSerializer


class IntIndDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = IntInd.objects.all()
    serializer_class = IntIndSerializer


# Text Inds
class TextIndListHandler(ListHandler):
    queryset = TextInd.objects.all()
    serializer_class = TextIndSerializer


class TextIndDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = TextInd.objects.all()
    serializer_class = TextIndSerializer


# Test Rec
class TestRecListHandler(ListCreateHandler):
    queryset = TestRec.objects.all()
    serializer_class = TestRecSerializer


class TestRecDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = TestRec.objects.all()
    serializer_class = TestRecSerializer


# Attachment
class AttachmentListHandler(ListCreateHandler):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class AttachmentDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


# Appointment
class AppointmentListHandler(ListCreateHandler):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


# Treatment
class TreatmentListHandler(ListCreateHandler):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer


class TreatmentDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer


# Medication
class MedicationListHandler(ListCreateHandler):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


class MedicationDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


# Diagnosis
class DiagnosisListHandler(ListCreateHandler):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer


class DiagnosisDetailHandler(RetrieveUpdateDestroyHandler):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
