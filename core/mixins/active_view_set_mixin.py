from ..models.activable_model import ActivableModel


class ActiveViewSetMixin:
    def get_queryset(self):
        if self.request.user.is_staff:
            model_class = self.serializer_class.Meta.model
            return model_class.active_objects.all() if isinstance(model_class,
                                                                  ActivableModel) else model_class.objects.all()
