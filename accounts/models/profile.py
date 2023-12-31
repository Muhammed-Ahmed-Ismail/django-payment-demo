from django.db import models

from django_extensions.db.models import TimeStampedModel

from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField()

    @property
    def name(self):
        return self.user.name

    @property
    def email(self):
        return self.user.email
