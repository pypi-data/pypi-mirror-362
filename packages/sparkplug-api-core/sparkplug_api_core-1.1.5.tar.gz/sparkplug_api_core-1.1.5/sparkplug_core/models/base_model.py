from django.db import models
from django_extensions.db.fields import ShortUUIDField


class BaseModel(models.Model):
    uuid = ShortUUIDField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "created"
        abstract = True

    @property
    def is_new(self) -> bool:
        # Check if creating a new instance
        return self._state.adding
