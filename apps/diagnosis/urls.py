from django.conf.urls import url
from apps.diagnosis.views import *

urlpatterns = [
    url(r'^show/(?P<diagnosis_id>\d+)$', show_action, name='show'),
    url(r'^(?P<patient_id>\d+)/create$', create_action, name='create'),
    url(r'^delete/(?P<diagnosis_id>\d+)$', delete_action, name='delete')
]
