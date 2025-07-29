from unittest.mock import patch

from django.test import TestCase

from sparkplug_avatars.factories import AvatarFactory
from sparkplug_avatars.utils.get_upload_location import get_upload_location


class TestGetUploadLocation(TestCase):
    @patch("sparkplug_avatars.utils.get_upload_location.time.time")
    def test_get_upload_location(self, mock_time):
        # Mock the current timestamp
        mock_time.return_value = 1672531200  # Example timestamp

        # Create an Avatar instance using the factory
        avatar = AvatarFactory(uuid="test-uuid")

        # Call the function with a sample filename
        filename = "example.jpg"
        upload_location = get_upload_location(avatar, filename)

        # Assert the upload location is correct
        assert upload_location == "avatars/test-uuid-1672531200.jpg"

    @patch("sparkplug_avatars.utils.get_upload_location.time.time")
    def test_get_upload_location_with_different_extension(self, mock_time):
        # Mock the current timestamp
        mock_time.return_value = 1672531200  # Example timestamp

        # Create an Avatar instance using the factory
        avatar = AvatarFactory(uuid="test-uuid")

        # Call the function with a sample filename with a different extension
        filename = "example.png"
        upload_location = get_upload_location(avatar, filename)

        # Assert the upload location is correct
        assert upload_location == "avatars/test-uuid-1672531200.png"
