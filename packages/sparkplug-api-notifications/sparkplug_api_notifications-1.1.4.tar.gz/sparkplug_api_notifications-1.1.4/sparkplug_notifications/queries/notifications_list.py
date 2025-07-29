from django.db.models import QuerySet
from sparkplug_core.utils import asdict_exclude_none

from ..models import Notification
from ..serializers import ListFilterData


def notifications_list(
    filters: ListFilterData,
) -> QuerySet["Notification"]:
    filter_kwargs = asdict_exclude_none(filters)
    return Notification.objects.filter(**filter_kwargs)
