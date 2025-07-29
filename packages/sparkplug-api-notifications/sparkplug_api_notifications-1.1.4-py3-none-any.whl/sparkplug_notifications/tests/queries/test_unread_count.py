from apps.users.factories import UserFactory
from django.test import TestCase
from freezegun import freeze_time

from sparkplug_notifications.factories import NotificationFactory
from sparkplug_notifications.queries import unread_count

from ..utils import create_partition_for_today


@freeze_time("2025-03-31")
class TestUnreadCount(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.user = UserFactory()
        self.user2 = UserFactory()
        self.user3 = UserFactory()

        # Create notifications for testing
        self.notification1 = NotificationFactory(
            recipient=self.user, has_read=False
        )
        self.notification2 = NotificationFactory(
            recipient=self.user, has_read=True
        )
        self.notification3 = NotificationFactory(
            recipient=self.user2, has_read=False
        )
        self.notification4 = NotificationFactory(
            recipient=self.user2, has_read=True
        )

    def test_unread_count_returns_correct_count(self):
        count = unread_count(self.user)
        assert count == 1

    def test_unread_count_returns_zero_when_no_unread_notifications(self):
        count = unread_count(self.user3)
        assert count == 0

    def test_unread_count_does_not_include_other_users_notifications(self):
        count = unread_count(self.user2)
        # Only one unread notification for user2
        assert count == 1

    def test_unread_count_with_multiple_unread_notifications(self):
        # Add another unread notification for self.user
        NotificationFactory(recipient=self.user, has_read=False)

        count = unread_count(self.user)
        assert count == 2  # Two unread notifications for self.user
