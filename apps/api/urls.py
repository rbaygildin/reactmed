from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from apps.api.views import *

urlpatterns = (
    # Create account
    url(r'^account$', SignupView.as_view(), name='account'),

    # Users
    url(r'^users$', UserListView.as_view(), name='users'),
    url(r'^user/(?P<pk>\d+)$', UserView.as_view(), name='user'),

    # Areas
    url(r'^areas$', MedAreaListView.as_view(), name='areas'),
    url(r'^area/(?P<pk>\d+)$', MedAreaView.as_view(), name='area'),

    # Tests
    url(r'^tests$', MedTestListView.as_view(), name='tests'),
    url(r'^test/(?P<pk>\d+)$', MedTestView.as_view(), name='test'),

    # Real Inds
    url(r'^real_inds$', RealIndListView.as_view(), name='real_inds'),
    url(r'^real_ind/(?P<pk>\d+)', RealIndView.as_view(), name='real_ind'),

    # Int Inds
    url(r'^int_inds$', IntIndListView.as_view(), name='int_inds'),
    url(r'^int_ind/(?P<pk>\d+)', IntIndView.as_view(), name='int_ind'),

    # Text Inds
    url(r'^text_inds$', TextIndListView.as_view(), name='text_inds'),
    url(r'^text_ind/(?P<pk>\d+)', TextIndView.as_view(), name='text_ind'),

    # Test Records
    url(r'^test_recs/(?P<patient_id>\d+)/(?P<test_type_id>.+)', csrf_exempt(TestRecListView.as_view()), name='test_recs')
)
