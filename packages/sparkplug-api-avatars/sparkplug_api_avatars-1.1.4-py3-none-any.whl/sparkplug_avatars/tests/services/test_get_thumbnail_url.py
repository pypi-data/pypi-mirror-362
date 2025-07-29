import io
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from sparkplug_avatars.factories import AvatarFactory
from sparkplug_avatars.services.get_thumbnail_url import get_thumbnail_url


class TestGetThumbnailUrl(TestCase):
    def create_in_memory_image(
        self, width, height, color="white", image_format="JPEG"
    ):
        """Create an in-memory image."""
        image = Image.new("RGB", (width, height), color=color)
        image_file = io.BytesIO()
        image.save(image_file, format=image_format)
        image_file.seek(0)
        return SimpleUploadedFile(
            "test.jpg",
            image_file.read(),
            content_type=f"image/{image_format.lower()}",
        )

    @patch("sparkplug_avatars.services.get_thumbnail_url.get_thumbnail")
    @patch("sparkplug_avatars.services.get_thumbnail_url.config")
    def test_get_thumbnail_url_with_crop(self, mock_config, mock_get_thumbnail):
        mock_config.return_value = "prod"

        # Use the helper method to create an in-memory image
        uploaded_file = self.create_in_memory_image(800, 600)

        # Create an avatar with the uploaded file
        avatar = AvatarFactory(file=uploaded_file)

        # Mock the return value of get_thumbnail
        mock_get_thumbnail.return_value.url = "/media/thumbnails/test.jpg"

        # Call the function under test
        url = get_thumbnail_url(
            avatar, crop_image=True, thumbnail_size="100x100"
        )

        # Assertions
        assert url == "/media/thumbnails/test.jpg"
        mock_get_thumbnail.assert_called_once_with(
            avatar.file,
            quality=100,
            crop="center",
            geometry_string="100x100",
        )

    @patch("sparkplug_avatars.services.get_thumbnail_url.get_thumbnail")
    @patch("sparkplug_avatars.services.get_thumbnail_url.config")
    def test_get_thumbnail_url_without_crop_landscape(
        self, mock_config, mock_get_thumbnail
    ):
        mock_config.return_value = "prod"

        # Use the helper method to create an in-memory image
        uploaded_file = self.create_in_memory_image(800, 600)

        # Create an avatar with the uploaded file
        avatar = AvatarFactory(file=uploaded_file)

        # Mock the return value of get_thumbnail
        mock_get_thumbnail.return_value.url = "/media/thumbnails/test.jpg"

        # Call the function under test
        url = get_thumbnail_url(
            avatar, crop_image=False, thumbnail_size="100x100"
        )

        # Assertions
        assert url == "/media/thumbnails/test.jpg"
        mock_get_thumbnail.assert_called_once_with(
            avatar.file,
            quality=100,
            geometry_string="100",
        )

    @patch("sparkplug_avatars.services.get_thumbnail_url.get_thumbnail")
    @patch("sparkplug_avatars.services.get_thumbnail_url.config")
    def test_get_thumbnail_url_without_crop_portrait(
        self, mock_config, mock_get_thumbnail
    ):
        mock_config.return_value = "prod"

        # Use the helper method to create an in-memory image
        uploaded_file = self.create_in_memory_image(600, 800)

        # Create an avatar with the uploaded file
        avatar = AvatarFactory(file=uploaded_file)

        # Mock the return value of get_thumbnail
        mock_get_thumbnail.return_value.url = "/media/thumbnails/test.jpg"

        # Call the function under test
        url = get_thumbnail_url(
            avatar, crop_image=False, thumbnail_size="100x100"
        )

        # Assertions
        assert url == "/media/thumbnails/test.jpg"
        mock_get_thumbnail.assert_called_once_with(
            avatar.file,
            quality=100,
            geometry_string="x100",
        )

    @patch("sparkplug_avatars.services.get_thumbnail_url.get_thumbnail")
    @patch("sparkplug_avatars.services.get_thumbnail_url.config")
    def test_get_thumbnail_url_in_dev_environment(
        self, mock_config, mock_get_thumbnail
    ):
        mock_config.return_value = "dev"

        # Use the helper method to create an in-memory image
        uploaded_file = self.create_in_memory_image(800, 600)

        # Create an avatar with the uploaded file
        avatar = AvatarFactory(file=uploaded_file)

        # Mock the return value of get_thumbnail
        mock_get_thumbnail.return_value.url = "/media/thumbnails/test.jpg"

        # Mock the API_URL setting
        with patch(
            "sparkplug_avatars.services.get_thumbnail_url.settings.API_URL",
            "http://localhost:8000",
        ):
            # Call the function under test
            url = get_thumbnail_url(
                avatar, crop_image=True, thumbnail_size="100x100"
            )

        # Assertions
        assert url == "http://localhost:8000/media/thumbnails/test.jpg"

    def test_get_thumbnail_url_with_no_file(self):
        avatar = AvatarFactory(file=None)

        url = get_thumbnail_url(
            avatar, crop_image=True, thumbnail_size="100x100"
        )

        assert url == ""
