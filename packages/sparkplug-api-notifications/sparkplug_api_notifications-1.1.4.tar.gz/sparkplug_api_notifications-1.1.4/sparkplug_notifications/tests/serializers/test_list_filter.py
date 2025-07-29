from apps.users.factories import UserFactory
from django.test import TestCase

from sparkplug_notifications.serializers.list_filter import (
    ListFilterData,
    ListFilterSerializer,
)


class TestListFilterSerializer(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_valid_data(self):
        data = {
            "recipient": self.user.id,
            "has_read": True,
            "is_starred": False,
        }
        serializer = ListFilterSerializer(data=data)
        assert serializer.is_valid()
        validated_data = serializer.validated_data
        assert isinstance(validated_data, ListFilterData)
        assert validated_data.recipient == self.user
        assert validated_data.has_read is True
        assert validated_data.is_starred is False

    def test_missing_optional_fields(self):
        data = {
            "recipient": self.user.id,
        }
        serializer = ListFilterSerializer(data=data)
        assert serializer.is_valid()
        validated_data = serializer.validated_data
        assert validated_data.has_read is None
        assert validated_data.is_starred is None

    def test_invalid_data(self):
        data = {
            "recipient": None,  # Invalid recipient
            "has_read": "invalid",  # Invalid boolean
        }
        serializer = ListFilterSerializer(data=data)
        assert not serializer.is_valid()
        assert "recipient" in serializer.errors
        assert "has_read" in serializer.errors
