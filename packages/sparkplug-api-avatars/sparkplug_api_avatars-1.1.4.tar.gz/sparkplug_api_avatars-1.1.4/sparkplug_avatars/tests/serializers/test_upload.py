from unittest.mock import MagicMock

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from sparkplug_avatars.serializers import UploadData, UploadSerializer


class TestUploadData(TestCase):
    def test_valid_file_extension(self):
        mock_file = MagicMock(spec=SimpleUploadedFile, name="image.jpg")
        data = UploadData(file=mock_file)
        assert data.file == mock_file

    def test_invalid_file_extension(self):
        mock_file = SimpleUploadedFile(
            "document.pdf",
            b"file_content",
            content_type="application/pdf",
        )
        with pytest.raises(ValidationError) as excinfo:
            UploadData(file=mock_file)
        assert "File must have one of the following extensions" in str(
            excinfo.value
        )


class TestUploadSerializer(TestCase):
    def test_serializer_with_valid_data(self):
        file = SimpleUploadedFile(
            "image.png",
            b"file_content",
            content_type="image/png",
        )
        data = {"file": file}
        serializer = UploadSerializer(data=data)
        assert serializer.is_valid()
        validated_data = serializer.validated_data
        assert validated_data.file == file

    def test_serializer_with_invalid_data(self):
        file = SimpleUploadedFile(
            "document.pdf",
            b"file_content",
            content_type="application/pdf",
        )
        data = {"file": file}
        serializer = UploadSerializer(data=data)
        assert not serializer.is_valid()
        assert "file" in serializer.errors
        assert (
            "File must have one of the following extensions: jpg, jpeg, png"
            in serializer.errors["file"]
        )
