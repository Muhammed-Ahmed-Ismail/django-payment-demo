from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes, action

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .serializers.user_serializer import UserSerializer

from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from .permissions.user_profile_permission import ProfileOwnerPermission
from .models.profile import Profile
from .serializers.profile_serializer import ProfileSerializer


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


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ProfileOwnerPermission]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False)
    def my_profile(self, request):
        # profile = Profile.objects.filter(user=request.user).first()
        profile = request.user.profile
        serializer = self.get_serializer(profile, many=False)
        return Response(data=serializer.data)
