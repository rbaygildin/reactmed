from django.conf.urls import url

from apps.appointments.views import *

urlpatterns = [
    url(r'^create$', create_action, name='create'),
    url(r'^show/(?P<appointment_id>\d+)$', show_action, name='show'),
    url(r'^finish/(?P<appointment_id>\d+)$', finish_action, name='finish'),
    url(r'^cancel/(?P<appointment_id>\d+)$', cancel_action, name='cancel'),
]
