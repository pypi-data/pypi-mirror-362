from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sparkplug_core.utils import (
    enforce_auth,
    get_paginated_response,
    get_validated_dataclass,
)

from ..queries import notifications_list
from ..serializers import DetailSerializer, ListFilterSerializer


class ListView(APIView):
    def get(self, request: Request) -> Response:
        enforce_auth("is_authenticated", request.user)

        filters = get_validated_dataclass(
            ListFilterSerializer,
            data={
                "recipient": request.user.id,
                "is_starred": request.query_params.get("is_starred"),
            },
        )

        queryset = (
            notifications_list(filters)
            .order_by("-created")
            .prefetch_related("recipient")
            .prefetch_related("actor")
        )

        return get_paginated_response(
            serializer_class=DetailSerializer,
            queryset=queryset,
            request=request,
            view=self,
        )
