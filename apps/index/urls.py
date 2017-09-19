from django.conf.urls import url
from apps.index.views import *

urlpatterns = [
    url(r'^$', index_page, name='index'),
    url(r'^about$', about_page, name='about')
]
