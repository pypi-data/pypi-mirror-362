from django.apps import AppConfig


class AvatarConfig(AppConfig):
    name = "sparkplug_avatars"

    def ready(self) -> None:
        from . import signals  # noqa: F401, PLC0415
