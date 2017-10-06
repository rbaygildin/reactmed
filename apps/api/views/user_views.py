from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from apps.core.models import User
from apps.api.serializers import UserSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
