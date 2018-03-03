from django.conf.urls import url

from apps.patients.views import *

urlpatterns = [
    url(r'^list$', list_action, name='list'),
    url(r'^tests$', tests_action, name='tests'),
    url(r'^appointments$', appointments_action, name='appointments'),
    url(r'^create$', create_action, name='create'),
    url(r'^update$', update_action, name='update'),
    url(r'^show/(?P<patient_id>\d+)$', show_action, name='show'),
    url(r'^delete/(?P<patient_id>\d+)$', delete_action, name='delete'),
    url(r'(?P<patient_id>\d+)/tests$', patient_test_action, name='patient_tests'),
    url(r'(?P<patient_id>\d+)/dynamics$', patient_dynamics_action, name='patient_dynamics'),
    url(r'(?P<patient_id>\d+)/appointments$', patient_appointments_action, name='patient_appointments'),
    url(r'(?P<patient_id>\d+)/diagnosis$', patient_diagnosis_action, name='patient_diagnosis'),
]
