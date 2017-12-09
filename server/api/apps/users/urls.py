from django.conf.urls import url
from apps.users.views import *

urlpatterns = [
    url(r'^show$', show_action, name='show'),
    url(r'^create$', create_action, name='create'),
    url(r'^update$', update_action, name='update'),
    url(r'^change_password$', change_password_action, name='change_password'),
    url(r'^reset_password$', reset_password_action, name='reset_password'),
    url(r'^delete$', delete_action, name='delete'),
    url(r'^logout$', logout_action, name='logout'),
    url(r'^dashboard$', dashboard_action, name='dashboard')
]
