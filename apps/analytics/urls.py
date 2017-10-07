from django.conf.urls import url
from apps.analytics.views import *

urlpatterns = [
    url(r'^visualize$', visualize_action, name='visualize'),
    url(r'^cluster$', cluster_action, name='cluster'),
    url(r'^data$', data_action, name='data'),
    url(r'^data/features/stat$', features_stat_action, name='features_stat')
]
