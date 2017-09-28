from django.conf.urls import url
from apps.users.views import *

urlpatterns = [
    url(r'^show$', show_view, name='show'),
    url(r'^create$', create_view, name='create'),
    url(r'^update$', update_user_view, name='update'),
    url(r'^change_password$', change_password_view, name='change_password'),
    url(r'^delete$', delete_view, name='delete'),
    url(r'^logout$', logout_view, name='logout')
]
