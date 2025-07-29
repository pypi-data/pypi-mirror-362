from dataclasses import dataclass

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_dataclasses.serializers import DataclassSerializer
from sparkplug_core.utils import (
    enforce_auth,
    get_validated_dataclass,
)
from sparkplug_core.views import WriteAPIView

from .. import services


@dataclass
class InputData:
    uuids: list[str]


class MarkReadView(WriteAPIView):
    """Marks notifications as read."""

    class InputSerializer(DataclassSerializer):
        class Meta:
            dataclass = InputData
            fields = ("uuids",)

    def patch(self, request: Request) -> Response:
        enforce_auth("is_authenticated", request.user)

        validated_data: InputData = get_validated_dataclass(
            self.InputSerializer,
            data=request.data,
        )

        services.mark_read(
            user=request.user,
            uuids=validated_data.uuids,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
