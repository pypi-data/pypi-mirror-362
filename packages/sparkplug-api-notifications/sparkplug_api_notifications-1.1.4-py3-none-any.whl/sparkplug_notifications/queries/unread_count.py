from typing import TYPE_CHECKING

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import QuerySet
from sparkplug_core.utils import get_validated_dataclass

from ..queries import notifications_list
from ..serializers import ListFilterSerializer

if TYPE_CHECKING:
    from ..models import Notification


def unread_count(
    recipient: type[AbstractBaseUser],
) -> QuerySet["Notification"]:
    validated_data = get_validated_dataclass(
        ListFilterSerializer,
        data={
            "recipient": recipient.id,
            "has_read": False,
        },
    )

    return notifications_list(validated_data).count()
