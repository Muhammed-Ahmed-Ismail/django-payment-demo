from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from .serializers.user_serializer import UserSerializer

from rest_framework import status


@api_view(['POST'])
@permission_classes([])
def signup(request):
    response = {'data': {}, 'status': status.HTTP_400_BAD_REQUEST}

    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user_serializer.save()
        response['data'] = user_serializer.data
        response['status'] = status.HTTP_201_CREATED
    return Response(**response)
