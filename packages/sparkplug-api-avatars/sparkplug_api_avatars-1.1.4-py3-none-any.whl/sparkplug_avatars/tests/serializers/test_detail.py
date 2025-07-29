from unittest.mock import patch

from apps.users.factories import UserFactory
from django.test import TestCase

from sparkplug_avatars.factories import AvatarFactory
from sparkplug_avatars.serializers.detail import AvatarDetailSerializer


class TestAvatarDetailSerializer(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.avatar = AvatarFactory(creator=self.user)

    @patch("sparkplug_avatars.serializers.detail.get_thumbnail_url")
    def test_serializer_with_valid_data(self, mock_get_thumbnail_url):
        mock_get_thumbnail_url.return_value = "http://example.com/thumbnail.jpg"

        serializer = AvatarDetailSerializer(instance=self.avatar)

        assert serializer.data["uuid"] == str(self.avatar.uuid)
        assert serializer.data[
            "created"
        ] == self.avatar.created.isoformat().replace("+00:00", "Z")
        assert serializer.data["creator_uuid"] == str(self.user.uuid)
        assert serializer.data["file"] == "http://example.com/thumbnail.jpg"

    def test_serializer_with_custom_thumbnail_size(self):
        serializer = AvatarDetailSerializer(
            instance=self.avatar,
            thumbnail_size="custom_size",
        )

        assert serializer.thumbnail_size == "custom_size"

    def test_serializer_with_crop_enabled(self):
        serializer = AvatarDetailSerializer(instance=self.avatar, crop=True)
        assert serializer.crop is True
