from djangorestframework_camel_case.parser import CamelCaseMultiPartParser
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from sparkplug_core.utils import (
    enforce_auth,
    get_validated_dataclass,
)
from sparkplug_core.views import WriteAPIView

from ..models import Avatar
from ..serializers import AvatarDetailSerializer, UploadData, UploadSerializer
from ..tasks import process_avatar_task


class UploadView(WriteAPIView):
    parser_classes = (CamelCaseMultiPartParser,)

    def post(self, request: Request) -> Response:
        enforce_auth("is_authenticated", request.user)

        validated_data: UploadData = get_validated_dataclass(
            UploadSerializer,
            data=request.data,
        )

        instance, _ = Avatar.objects.update_or_create(
            creator=request.user,
            defaults={"file": validated_data.file},
        )

        process_avatar_task(instance.uuid)()

        return Response(
            data=AvatarDetailSerializer(instance).data,
            status=status.HTTP_200_OK,
        )
