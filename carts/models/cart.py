from django.db import models
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
