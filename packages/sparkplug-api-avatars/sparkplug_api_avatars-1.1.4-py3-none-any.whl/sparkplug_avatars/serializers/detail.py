from django.conf import settings
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    Serializer,
    SerializerMethodField,
)

from ..models import Avatar
from ..services import get_thumbnail_url


class AvatarDetailSerializer(Serializer):
    uuid = CharField()
    created = DateTimeField()
    creator_uuid = SerializerMethodField()
    file = SerializerMethodField()

    def __init__(self, *args, **kwargs) -> None:
        self.crop = kwargs.pop("crop", False)
        self.thumbnail_size = kwargs.pop(
            "thumbnail_size",
            settings.THUMBNAIL_PRESET_DEFAULT,
        )
        super().__init__(*args, **kwargs)

    def get_creator_uuid(self, obj: Avatar) -> str:
        return obj.creator.uuid

    def get_file(self, obj: Avatar) -> str:
        return get_thumbnail_url(
            obj,
            self.thumbnail_size,
            crop_image=self.crop,
        )
