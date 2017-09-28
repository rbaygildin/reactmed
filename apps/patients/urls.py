from django.conf.urls import url

from apps.patients.views import *

urlpatterns = [
    url(r'^list$', list_action, name='list'),
    url(r'^create$', create_action, name='create'),
    url(r'^show/(?P<patient_id>\d+)$', show_action, name='show')
]
