from django.conf.urls import url
from apps.accounts.views import *

urlpatterns = [
    url(r'^show$', show_view, name='show'),
    url(r'^create$', create_account_view, name='create')
]
