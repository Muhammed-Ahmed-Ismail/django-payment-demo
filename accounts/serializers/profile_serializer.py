from rest_framework import serializers
from ..models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'name', 'address')

    def get_name(self, profile):
        return profile.user.first_name + profile.user.last_name

    def get_username(self, profile):
        return profile.user.username
