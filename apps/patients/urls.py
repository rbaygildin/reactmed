from django.conf.urls import url

from apps.patients.views import *

urlpatterns = [
    url(r'^create$', create_action, name='create'),
    url(r'^update$', update_action, name='update'),
    url(r'^show/(?P<patient_id>\d+)$', show_action, name='show'),
    url(r'^delete/(?P<patient_id>\d+)$', delete_action, name='delete')
]
