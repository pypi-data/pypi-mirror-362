import logging

from huey.contrib.djhuey import task

from ..services import process_avatar

log = logging.getLogger(__name__)


@task()
def process_avatar_task(avatar_uuid: str) -> None:
    process_avatar(avatar_uuid)
