from typing import ClassVar

from django.conf import settings
from django.db import models
from psqlextra.models import PostgresPartitionedModel
from psqlextra.types import PostgresPartitioningMethod
from sparkplug_core.models import BaseModel


class Notification(
    PostgresPartitionedModel,
    BaseModel,
):
    recipient = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    has_read = models.BooleanField(
        default=False,
    )

    is_starred = models.BooleanField(
        default=False,
    )

    actor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
    )

    actor_text = models.CharField(
        max_length=255,
    )

    message = models.CharField(
        max_length=255,
    )

    target_route = models.JSONField(
        null=True,
    )

    class Meta:
        indexes = (models.Index(fields=["uuid"]),)
        ordering = ("-created",)

    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key: ClassVar = ["created"]

    def __str__(self) -> str:
        return f"{self.recipient} - {self.message}"
