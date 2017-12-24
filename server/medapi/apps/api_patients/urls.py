from django.conf.urls import url

from apps.api_patients.views import PatientApiView

patient_list = PatientApiView.as_view({
    'get': 'list',
    'post': 'create'
})

patient_detail = PatientApiView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    url(r'^$', patient_list, name='patients'),
    url(r'^(?P<pk>\d+)$', patient_detail, name='patient')
]
