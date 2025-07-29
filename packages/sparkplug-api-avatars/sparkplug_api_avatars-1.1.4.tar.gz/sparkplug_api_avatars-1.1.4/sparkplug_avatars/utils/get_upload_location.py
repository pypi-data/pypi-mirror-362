import time
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Avatar


def get_upload_location(instance: "Avatar", filename: str) -> str:
    path = Path(filename)
    extension = path.suffix

    # cast from float to int to remove decimal precision
    timestamp = int(time.time())

    # create unique filenames to avoid stale cache
    filename = f"{instance.uuid}-{timestamp}"

    return f"avatars/{filename}{extension}"
