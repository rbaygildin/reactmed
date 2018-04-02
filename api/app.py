import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
django.setup()

from tornado.options import options, define, parse_command_line
from apps.dicom_ws.handlers import *
import tornado.httpserver
from tornado.ioloop import IOLoop
from tornado.web import Application
import tornado.wsgi

define('port', type=int, default=8080)

PATIENT_LIST_URL = r'/api/patients'
PATIENT_DETAIL_URL = r'/api/patients/(\d+)'


def main():
    parse_command_line()
    app = Application(
        [
            (PATIENT_LIST_URL, PatientListHandler),
            (PATIENT_DETAIL_URL, PatientDetailHandler)
        ]
    )
    app.start(0)
    IOLoop.current().start()
    pass


if __name__ == '__main__':
    main()
