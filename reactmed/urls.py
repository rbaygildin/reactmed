"""reactmed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('apps.api.urls', namespace='api')),
    url(r'', include('apps.main.urls', namespace='main')),
    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^patients/', include('apps.patients.urls', namespace='patients')),
    url(r'^med_tests/', include('apps.med_tests.urls', namespace='med_tests')),
    url(r'^appointments/', include('apps.appointments.urls', namespace='appointments')),
    url(r'^diagnosis/', include('apps.diagnosis.urls', namespace='diagnosis')),
    url(r'^reports/', include('apps.reports.urls', namespace='reports')),
    url(r'^analytics/', include('apps.analytics.urls', namespace='analytics'))
]
