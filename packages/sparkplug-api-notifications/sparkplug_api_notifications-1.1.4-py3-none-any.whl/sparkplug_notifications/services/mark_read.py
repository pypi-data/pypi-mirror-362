from django.contrib.auth.base_user import AbstractBaseUser

from ..models import Notification


def mark_read(user: type[AbstractBaseUser], uuids: list[str]) -> None:
    Notification.objects.filter(recipient=user, uuid__in=uuids).update(
        has_read=True
    )
