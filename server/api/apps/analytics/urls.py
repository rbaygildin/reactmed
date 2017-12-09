from django.conf.urls import url
from apps.analytics.views import *

urlpatterns = [
    url(r'^visualize$', visualize_action, name='visualize'),
    url(r'^cluster$', cluster_action, name='cluster'),
    url(r'^data$', data_action, name='data'),
    url(r'^data/features/stat$', features_stat_action, name='features_stat'),
    url(r'^datasets$', datasets_page_action, name='datasets'),
    url(r'^visualization$', visualize_page_action, name='visualization'),
    url(r'^clustering$', clustering_page_action, name='clustering')
]
