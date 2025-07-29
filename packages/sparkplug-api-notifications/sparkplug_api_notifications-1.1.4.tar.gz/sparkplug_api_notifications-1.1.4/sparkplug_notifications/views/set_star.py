from dataclasses import dataclass

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_dataclasses.serializers import DataclassSerializer
from sparkplug_core.utils import (
    enforce_auth,
    enforce_permission,
    get_validated_dataclass,
)
from sparkplug_core.views import WriteAPIView

from ..models import Notification


@dataclass
class InputData:
    is_starred: bool


class SetStarView(WriteAPIView):
    """Sets the `is_starred` field for a notification."""

    class InputSerializer(DataclassSerializer):
        class Meta:
            dataclass = InputData

    def patch(self, request: Request, uuid: str) -> Response:
        enforce_auth("is_authenticated", request.user)
        notification = get_object_or_404(Notification, uuid=uuid)
        enforce_permission("is_recipient", notification, request.user)

        validated_data: InputData = get_validated_dataclass(
            self.InputSerializer,
            data=request.data,
        )

        notification.is_starred = validated_data.is_starred
        notification.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
