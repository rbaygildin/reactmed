from django.conf.urls import url
from apps.reports.views import *

urlpatterns = [
    url(r'^tests/(?P<test_id>\d+)', generate_test_report_action, name='test')
]
