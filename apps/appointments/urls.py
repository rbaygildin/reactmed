from django.conf.urls import url

from apps.appointments.views import *

urlpatterns = [
    url(r'^create$', create_action, name='create'),
    url(r'^show/(?P<appointment_id>\d+)$', show_action, name='show')
]
