from django.conf.urls import url
from apps.analytics.views import *

urlpatterns = [
    url(r'^visualize$', visualize_action, name='visualize'),
    # url(r'^cluster$', cluster_action, name='cluster'),
    url(r'^data$', data_action, name='data'),
    # url(r'^data_stat$', data_stat_action, name='data_stat')
]
