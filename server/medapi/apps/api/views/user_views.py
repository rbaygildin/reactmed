from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import *

from apps.core.models import User
from apps.api.serializers import UserSerializer


class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(RetrieveUpdateDestroyAPIView):
    """
    Rest endpoint presents user in system,
    provide authentication, permissions and CRUD
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


def check_login(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return JsonResponse(data={'error': 'Пользователь с таким логином не существует!'})
        if not user.check_password(password):
            return JsonResponse(data={'error': 'Пароль введен неправильно!'})
    return JsonResponse(data={})
