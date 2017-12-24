from django.contrib import auth
from django.http import JsonResponse
from rest_framework.decorators import detail_route, api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet

from apps.api.serializers import UserSerializer
from apps.core.models import User


class UserApiView(ModelViewSet):
    """
    Rest endpoint presents all users in system
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['post'], persmission_classes=[IsAuthenticated, IsAdminUser])
    def create(self, request, *args, **kwargs):
        """
        Create user account
        """
        return super(UserApiView, self).create(request, args, kwargs)

    @detail_route(methods=['get'], persmission_classes=[IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        """
        Find user account by id
        """
        return super(UserApiView, self).retrieve(request, args, kwargs)

    @detail_route(methods=['get'], persmission_classes=[IsAuthenticated, IsAdminUser])
    def list(self, request, *args, **kwargs):
        """
        Find all users
        """
        return super(UserApiView, self).list(request, args, kwargs)

    @detail_route(methods=['retrieve'], persmission_classes=[IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Update user information
        """
        return super(UserApiView, self).update(request, args, kwargs)

    @detail_route(methods=['delete'], persmission_classes=[IsAuthenticated, IsAdminUser])
    def destroy(self, request, *args, **kwargs):
        """
        Delete user account
        """
        return super(UserApiView, self).destroy(request, args, kwargs)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request, pk):
    """
    Change users password
    """
    password = request.PUT.get('password')
    request.user.set_password(password)
    request.user.save()
    return JsonResponse(data={'message': 'Пароль успешно изменен'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_email(request, pk):
    """
    Change users email
    """
    email = request.PUT.get('email')
    request.user.email = email
    request.user.save()
    return JsonResponse(data={'message': 'Электронная почта успешно изменена'})


@api_view(['POST'])
def login(request):
    """
    Login user in system
    """
    username = request.GET.get('username')
    password = request.GET.get('password')
    try:
        user = User.objects.get(email=username)
    except User.DoesNotExist:
        return JsonResponse(data={'error': 'Пользователь с таким логином не существует!'})
    if not user.check_password(password):
        return JsonResponse(data={'error': 'Пароль введен неправильно!'})

    return JsonResponse(data={'message': 'Успешная аутентификация'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout user
    """
    auth.logout(request)
    return JsonResponse(data={'message': 'Пользователь вышел из своей учетной записи'})
