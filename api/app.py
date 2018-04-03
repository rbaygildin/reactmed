#!/usr/bin/env python
import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
django.setup()

from tornado.options import options, define, parse_command_line
from apps.api.handlers import *
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

define('rest_port', type=int, default=8080)

# Users
USER_LIST_URL = r'/api/users'
USER_DETAIL_URL = r'/api/users/(\d+)'
USER_LOGIN_URL = r'/api/users/auth/login'
USER_LOGOUT_URL = r'/api/users/auth/logout'

# Patients
PATIENT_LIST_URL = r'/api/patients'
PATIENT_DETAIL_URL = r'/api/patients/(\d+)'

# Med areas
MED_AREA_LIST_URL = r'/api/med_areas'
MED_AREA_DETAIL_URL = r'/api/med_areas/(\d+)'

# Med tests
MED_TEST_LIST_URL = r'/api/med_tests'
MED_TEST_DETAIL_URL = r'/api/med_tests/(\d+)'

# Real inds
REAL_IND_LIST_URL = r'/api/real_inds'
REAL_IND_DETAIL_URL = r'/api/real_inds/(\d+)'

# Int inds
INT_IND_LIST_URL = r'/api/int_inds'
INT_IND_DETAIL_URL = r'/api/int_inds/(\d+)'

# Text inds
TEXT_IND_LIST_URL = r'/api/text_inds'
TEXT_IND_DETAIL_URL = r'/api/text_inds/(\d+)'

# Test recs
TEST_REC_LIST_URL = r'/api/test_recs'
TEST_REC_DETAIL_URL = r'/api/test_recs/(\d+)'

# Attachments
ATTACHMENT_LIST_URL = r'/api/attachment'
ATTACHMENT_DETAIL_URL = r'/api/attachment/(\d+)'

# Appointment
APPOINTMENT_LIST_URL = r'/api/appointments'
APPOINTMENT_DETAIL_URL = r'/api/appointments/(\d+)'

# Treatments
TREATMENT_LIST_URL = r'/api/treatments'
TREATMENT_DETAIL_URL = r'/api/treatments/(\d+)'

# Medications
MEDICATION_LIST_URL = r'/api/medications'
MEDICATION_DETAIL_URL = r'/api/medications/(\d+)'

# Diagnosis
DIAGNOSIS_LIST_URL = r'/api/diagnoses'
DIAGNOSIS_DETAIL_URL = r'/api/diagnoses/(\d+)'

MEDIA_URL = r'/media/(.*)'


def main():
    parse_command_line()
    rest_app = tornado.web.Application(
        [
            # Users
            (USER_DETAIL_URL, UserDetailHandler),
            (USER_LIST_URL, UserListHandler),

            # Patients
            (PATIENT_DETAIL_URL, PatientDetailHandler),
            (PATIENT_LIST_URL, PatientListHandler),

            # Med areas
            (MED_AREA_DETAIL_URL, MedAreaDetailHandler),
            (MED_AREA_LIST_URL, MedAreaListHandler),

            # Med tests
            (MED_TEST_DETAIL_URL, MedTestDetailHandler),
            (MED_TEST_LIST_URL, MedTestListHandler),

            # Real inds
            (REAL_IND_DETAIL_URL, RealIndDetailHandler),
            (REAL_IND_LIST_URL, RealIndListHandler),

            # Int inds
            (INT_IND_DETAIL_URL, IntIndDetailHandler),
            (INT_IND_LIST_URL, IntIndListHandler),

            # Text inds
            (TEXT_IND_DETAIL_URL, TextIndDetailHandler),
            (TEXT_IND_LIST_URL, TextIndListHandler),

            # Test recs
            (TEST_REC_DETAIL_URL, TestRecDetailHandler),
            (TEST_REC_LIST_URL, TestRecListHandler),

            # Appointments
            (APPOINTMENT_DETAIL_URL, AppointmentDetailHandler),
            (APPOINTMENT_LIST_URL, AppointmentListHandler),

            # Treatments
            (TREATMENT_DETAIL_URL, TreatmentDetailHandler),
            (TREATMENT_LIST_URL, TreatmentListHandler),

            # Medications
            (MEDICATION_DETAIL_URL, MedicationDetailHandler),
            (MEDICATION_LIST_URL, MedicationListHandler),

            # Diagnoses
            (DIAGNOSIS_DETAIL_URL, DiagnosisDetailHandler),
            (DIAGNOSIS_LIST_URL, DiagnosisListHandler),

            # Media download
            (MEDIA_URL, tornado.web.StaticFileHandler, {'path': 'media'})
        ])
    rest_server = tornado.httpserver.HTTPServer(rest_app)
    rest_server.bind(options.rest_port)
    rest_server.start()
    print('HTTP server started')
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
