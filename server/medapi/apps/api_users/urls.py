from django.conf.urls import url
from apps.api_users.views import *

user_list = UserApiView.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserApiView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^(?P<pk>\d+)/change_password$', logout, name='change_password'),
    url(r'^(?P<pk>\d+)/change_email$', logout, name='change_email'),
    url(r'^(?P<pk>\d+)$', user_detail, name='user'),
    url(r'^$', user_list, name='users'),
]
