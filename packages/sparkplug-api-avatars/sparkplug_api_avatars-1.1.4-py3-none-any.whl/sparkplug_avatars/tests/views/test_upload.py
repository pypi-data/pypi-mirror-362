from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from apps.users.factories import UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from sparkplug_avatars.models import Avatar

TEST_MEDIA_ROOT = Path(__file__).parent / "test_media"


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class TestUploadViewIntegration(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.raise_request_exception = True
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("sparkplug_avatars:upload")

    def tearDown(self):
        for avatar in Avatar.objects.all():
            if avatar.file:
                avatar.file.delete(save=False)

    @patch("sparkplug_avatars.views.upload.process_avatar_task")
    def test_upload_view_creates_avatar(self, mock_process_avatar_task):
        image = Image.new("RGB", (10, 10), color="red")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        file = SimpleUploadedFile(
            "avatar.jpg",
            buffer.read(),
            content_type="image/jpeg",
        )

        response = self.client.post(
            self.url,
            data={"file": file},
            format="multipart",
        )

        assert response.status_code == status.HTTP_200_OK
        assert Avatar.objects.filter(creator=self.user).exists()
        avatar = Avatar.objects.get(creator=self.user)
        # The file name should be avatars/<uuid>-<timestamp>.jpg
        assert avatar.file.name.startswith(f"avatars/{avatar.uuid}-")
        assert avatar.file.name.endswith(".jpg")
        assert response.data["uuid"] == avatar.uuid

    def test_upload_view_requires_auth(self):
        self.client.force_authenticate(user=None)
        file = SimpleUploadedFile(
            "avatar.jpg",
            b"dummy",
            content_type="image/jpeg",
        )

        response = self.client.post(
            self.url,
            data={"file": file},
            format="multipart",
        )

        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_upload_view_invalid_data(self):
        file = SimpleUploadedFile(
            "invalid.txt",
            b"not an image",
            content_type="text/plain",
        )

        response = self.client.post(
            self.url,
            data={"file": file},
            format="multipart",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not Avatar.objects.filter(creator=self.user).exists()
