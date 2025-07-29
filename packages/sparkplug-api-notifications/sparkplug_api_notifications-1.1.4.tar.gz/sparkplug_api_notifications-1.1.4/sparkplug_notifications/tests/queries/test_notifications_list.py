from apps.users.factories import UserFactory
from django.test import TestCase
from freezegun import freeze_time

from sparkplug_notifications.factories import NotificationFactory
from sparkplug_notifications.queries import notifications_list
from sparkplug_notifications.serializers import ListFilterData

from ..utils import create_partition_for_today


@freeze_time("2025-03-31")
class TestNotificationsList(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.user = UserFactory()
        self.other_user = UserFactory()

        # Create notifications for testing
        self.notification1 = NotificationFactory(
            recipient=self.user,
            has_read=False,
            is_starred=True,
        )
        self.notification2 = NotificationFactory(
            recipient=self.user,
            has_read=True,
            is_starred=False,
        )
        self.notification3 = NotificationFactory(
            recipient=self.other_user,
            has_read=False,
            is_starred=True,
        )

    def test_notifications_list_with_recipient_filter(self):
        filters = ListFilterData(recipient=self.user)
        queryset = notifications_list(filters)

        assert self.notification1 in queryset
        assert self.notification2 in queryset
        assert self.notification3 not in queryset

    def test_notifications_list_with_has_read_filter(self):
        filters = ListFilterData(recipient=self.user, has_read=True)
        queryset = notifications_list(filters)

        assert self.notification1 not in queryset
        assert self.notification2 in queryset

    def test_notifications_list_with_is_starred_filter(self):
        filters = ListFilterData(recipient=self.user, is_starred=True)
        queryset = notifications_list(filters)

        assert self.notification1 in queryset
        assert self.notification2 not in queryset

    def test_notifications_list_with_combined_filters(self):
        filters = ListFilterData(
            recipient=self.user,
            has_read=False,
            is_starred=True,
        )
        queryset = notifications_list(filters)

        assert self.notification1 in queryset
        assert self.notification2 not in queryset
        assert self.notification3 not in queryset
