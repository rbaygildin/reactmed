from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.rest.serializers import SignupSerializer


class SignupView(APIView):

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
