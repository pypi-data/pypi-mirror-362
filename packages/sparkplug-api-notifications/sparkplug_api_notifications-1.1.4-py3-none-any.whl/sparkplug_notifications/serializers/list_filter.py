from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer


@dataclass
class ListFilterData:
    recipient: AbstractBaseUser
    has_read: bool | None = None
    is_starred: bool | None = None


class ListFilterSerializer(DataclassSerializer):
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        dataclass = ListFilterData
