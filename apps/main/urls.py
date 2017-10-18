from django.conf.urls import url
from apps.main.views import *

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^about$', about_view, name='about'),
    url(r'^help$', help_view, name='help'),
    url(r'^login$', login_view, name='login'),
    url(r'^help/med_tests/(?P<test_id>\d+)$', show_med_test_help, name='show_med_test_help'),
    url(r'^help/med_tests$', med_tests_help, name='med_tests_help'),
    url(r'^on_fail/login$', on_fail_login, name='on_fail_login')
]
