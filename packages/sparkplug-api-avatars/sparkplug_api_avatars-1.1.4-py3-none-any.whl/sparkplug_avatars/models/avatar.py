from django.conf import settings
from django.db import models
from sorl.thumbnail import ImageField
from sparkplug_core.models import BaseModel

from ..utils import get_upload_location


class Avatar(BaseModel):
    creator = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
    )

    file = ImageField(
        upload_to=get_upload_location,
    )

    class Meta:
        indexes = (models.Index(fields=["uuid"]),)

    def __str__(self) -> str:
        return self.uuid

    def delete(self, *args, **kwargs) -> None:
        self.file.delete()
        super().delete(*args, **kwargs)
