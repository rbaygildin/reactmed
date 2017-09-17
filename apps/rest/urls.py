from django.conf.urls import url

from apps.rest.views import *

urlpatterns = (
    # Areas
    url(r'^areas$', MedAreaListView.as_view()),
    url(r'^area/(?P<pk>\d+)$', MedAreaView.as_view()),

    # Tests
    url(r'^tests$', MedTestListView.as_view()),
    url(r'^test/(?P<pk>\d+)$', MedTestView.as_view()),

    # Real Inds
    url(r'^real_inds$', RealIndListView.as_view()),
    url(r'^real_ind/(?P<pk>\d+)', RealIndView.as_view()),

    # Int Inds
    url(r'^int_inds$', IntIndListView.as_view()),
    url(r'^int_ind/(?P<pk>\d+)', IntIndView.as_view()),

    # Text Inds
    url(r'^text_inds$', TextIndListView.as_view()),
    url(r'^text_ind/(?P<pk>\d+)', TextIndView.as_view()),
)
