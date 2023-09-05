from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Password and confirm password must match')

        return data

    def save(self, **kwargs):
        User = get_user_model()
        user = User(username=self.validated_data.get('username'))
        user.set_password(self.validated_data.get('password'))
        user.save()
