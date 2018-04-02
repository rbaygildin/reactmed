import json

from django.http import HttpResponse


def return_hello(request):
    return HttpResponse(json.dumps({'name': 'alex'}), content_type='application/json')
