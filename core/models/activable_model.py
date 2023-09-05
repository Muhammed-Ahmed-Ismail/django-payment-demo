from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ActivableModel(models.Model):
    # active_objects = ActiveManager()

    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
