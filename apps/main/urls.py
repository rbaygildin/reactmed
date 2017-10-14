from django.conf.urls import url
from apps.main.views import *

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^about$', about_view, name='about'),
    url(r'^help$', help_view, name='help'),
    url(r'^login$', login_view, name='login')
]
