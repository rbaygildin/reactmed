from django.conf.urls import url
from apps.api_tests.views import *

med_area_list = MedAreaApiViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

med_area_detail = MedAreaApiViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

med_test_list = MedTestApiViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

med_test_detail = MedTestApiViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

test_rec_list = TestRecApiViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

test_rec_detail = TestRecApiViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    url(r'^med_areas$', med_area_list, name='med_areas'),
    url(r'^med_areas/(?P<pk>\d+)$', med_area_detail, name='med_area'),
    url(r'^med_tests$', med_test_list, name='med_tests'),
    url(r'^med_tests/(?P<pk>\d+)$', med_test_detail, name='med_test'),
    url(r'^test_recs$', test_rec_list, name='test_recs'),
    url(r'^test_recs/(?P<pk>\d+)$', test_rec_detail, name='test_rec')
]
