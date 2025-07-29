from dataclasses import dataclass
from typing import ClassVar

from django.core.files import File
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FileField
from rest_framework_dataclasses.serializers import DataclassSerializer


@dataclass
class UploadData:
    file: File

    def __post_init__(self) -> None:
        allowed_extensions = ["jpg", "jpeg", "png"]
        if not any(self.file.name.endswith(ext) for ext in allowed_extensions):
            ext_msg = ", ".join(allowed_extensions)
            msg = f"File must have one of the following extensions: {ext_msg}"
            raise ValidationError({"file": msg})


class UploadSerializer(DataclassSerializer):
    serializer_field_mapping: ClassVar = {
        **DataclassSerializer.serializer_field_mapping,
        File: FileField,
    }

    class Meta:
        dataclass = UploadData
