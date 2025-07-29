from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sparkplug_core.utils import enforce_auth

from ..queries import unread_count


class UnreadCountView(APIView):
    def get(self, request: Request) -> Response:
        """Get the user's unread notifications count."""
        enforce_auth("is_authenticated", request.user)

        return Response(
            status=status.HTTP_200_OK,
            data=unread_count(request.user),
        )
