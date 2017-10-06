from django.conf.urls import url

from apps.med_tests.views import *

urlpatterns = [
    url(r'^create$', create_action, name='create'),
    url(r'^show/(?P<test_id>\d+)$', show_action, name='show'),
    url(r'^delete/(?P<test_id>\d+)', delete_action, name='delete'),
    url(r'^dynamics$', dynamics_action, name='dynamics')
]
