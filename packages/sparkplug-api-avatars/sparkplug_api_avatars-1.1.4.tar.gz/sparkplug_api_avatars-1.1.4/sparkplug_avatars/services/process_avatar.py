import logging
from pathlib import Path

from decouple import config
from django.core.files import File

from .. import models
from .image_optimizer import ImageOptimizer

log = logging.getLogger(__name__)

MAX_LENGTH = 240


def process_avatar(avatar_uuid: str) -> None:
    try:
        instance = models.Avatar.objects.get(uuid=avatar_uuid)
    except models.Avatar.DoesNotExist:
        return

    if bool(instance.file) is False:
        return

    log.debug(
        "process avatar",
        extra={"avatar_uuid": instance.uuid},
    )

    environment = config("API_ENV")

    source = instance.file.url
    if environment == "dev":
        source = instance.file.path

    log.debug(
        "avatar source",
        extra={"avatar_source": source},
    )

    try:
        filepath, optimized = ImageOptimizer(
            source=source,
            filename=instance.uuid,
            max_long=MAX_LENGTH,
            max_short=MAX_LENGTH,
        ).optimize()

        if not optimized:
            return

        with Path.open(filepath, "rb") as f:
            file = File(f)
            filename = Path(filepath).name

            if instance.file:
                instance.file.delete()

            instance.file.save(filename, file)

        log.info(
            "Optimized avatar image",
            extra={
                "image_id": instance.id,
            },
        )

    except FileNotFoundError:
        log.exception(
            "Failed to optimize image",
            extra={
                "image_uuid": instance.uuid,
                "image_source": source,
            },
        )
