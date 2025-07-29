from unittest.mock import MagicMock, patch

from django.test import TestCase

from sparkplug_avatars import models
from sparkplug_avatars.factories import AvatarFactory
from sparkplug_avatars.services.process_avatar import process_avatar


class TestProcessAvatar(TestCase):
    @patch(
        "sparkplug_avatars.services.process_avatar.models.Avatar.objects.get"
    )
    @patch("sparkplug_avatars.services.process_avatar.ImageOptimizer")
    @patch("sparkplug_avatars.services.process_avatar.File")
    @patch("sparkplug_avatars.services.process_avatar.Path.open")
    @patch("sparkplug_avatars.services.process_avatar.config")
    def test_process_avatar_success(
        self,
        mock_config,
        mock_path_open,
        mock_file,
        mock_image_optimizer,
        mock_avatar_get,
    ):
        # Arrange
        mock_avatar = AvatarFactory.build(file=MagicMock())
        mock_avatar_get.return_value = mock_avatar
        mock_config.return_value = "dev"
        mock_image_optimizer.return_value.optimize.return_value = (
            "/tmp/test.jpg",
            True,
        )
        mock_path_open.return_value.__enter__.return_value = MagicMock()

        # Act
        process_avatar(mock_avatar.uuid)

        # Assert
        mock_avatar_get.assert_called_once_with(uuid=mock_avatar.uuid)
        mock_image_optimizer.assert_called_once_with(
            source=mock_avatar.file.path,
            filename=mock_avatar.uuid,
            max_long=240,
            max_short=240,
        )
        mock_avatar.file.delete.assert_called_once()
        mock_avatar.file.save.assert_called_once_with(
            "test.jpg",
            mock_file(mock_path_open.return_value.__enter__.return_value),
        )

    @patch(
        "sparkplug_avatars.services.process_avatar.models.Avatar.objects.get"
    )
    def test_process_avatar_avatar_does_not_exist(self, mock_avatar_get):
        # Arrange
        mock_avatar_get.side_effect = models.Avatar.DoesNotExist

        # Act
        process_avatar("nonexistent-uuid")

        # Assert
        mock_avatar_get.assert_called_once_with(uuid="nonexistent-uuid")

    @patch(
        "sparkplug_avatars.services.process_avatar.models.Avatar.objects.get"
    )
    def test_process_avatar_no_file(self, mock_avatar_get):
        # Arrange
        mock_avatar = AvatarFactory.build(file=None)
        mock_avatar_get.return_value = mock_avatar

        # Act
        process_avatar(mock_avatar.uuid)

        # Assert
        mock_avatar_get.assert_called_once_with(uuid=mock_avatar.uuid)

    @patch(
        "sparkplug_avatars.services.process_avatar.models.Avatar.objects.get"
    )
    @patch("sparkplug_avatars.services.process_avatar.ImageOptimizer")
    def test_process_avatar_not_optimized(
        self, mock_image_optimizer, mock_avatar_get
    ):
        # Arrange
        mock_avatar = AvatarFactory.build(file=MagicMock())
        mock_avatar_get.return_value = mock_avatar
        mock_image_optimizer.return_value.optimize.return_value = (
            "/tmp/test.jpg",
            False,
        )

        # Act
        process_avatar(mock_avatar.uuid)

        # Assert
        mock_avatar_get.assert_called_once_with(uuid=mock_avatar.uuid)
        mock_image_optimizer.assert_called_once()
        mock_avatar.file.delete.assert_not_called()
        mock_avatar.file.save.assert_not_called()

    @patch(
        "sparkplug_avatars.services.process_avatar.models.Avatar.objects.get"
    )
    @patch("sparkplug_avatars.services.process_avatar.Path.open")
    @patch("sparkplug_avatars.services.process_avatar.log")
    @patch("sparkplug_avatars.services.image_optimizer.Image.open")
    def test_process_avatar_file_not_found(
        self,
        mock_image_open,
        mock_log,
        mock_path_open,
        mock_avatar_get,
    ):
        # Arrange
        mock_avatar = AvatarFactory.build(file=MagicMock())
        mock_avatar_get.return_value = mock_avatar
        mock_image_open.side_effect = FileNotFoundError

        # Act
        process_avatar(mock_avatar.uuid)

        # Assert
        mock_avatar_get.assert_called_once_with(uuid=mock_avatar.uuid)
        mock_log.exception.assert_called_once_with(
            "Failed to optimize image",
            extra={
                "image_uuid": mock_avatar.uuid,
                "image_source": mock_avatar.file.url,
            },
        )
