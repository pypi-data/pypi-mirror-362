# ruff: noqa: ARG001, ANN001
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Avatar


@receiver(pre_save, sender=Avatar)
def avatar_pre_save(sender, instance, **kwargs) -> None:
    try:
        previous = Avatar.objects.get(uuid=instance.uuid)
    except Avatar.DoesNotExist:
        previous = None

    if not previous:
        return

    if previous.file != instance.file:
        previous.file.delete(save=False)
