from apps.users.factories import UserFactory
from django.test import TestCase
from freezegun import freeze_time

from sparkplug_notifications.factories import NotificationFactory
from sparkplug_notifications.services import mark_read

from ..utils import create_partition_for_today


@freeze_time("2025-03-31")
class TestMarkRead(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.user = UserFactory()
        self.other_user = UserFactory()

    def test_mark_read_marks_notifications_as_read(self):
        # Create notifications for this test
        notification1 = NotificationFactory(recipient=self.user, has_read=False)
        notification2 = NotificationFactory(recipient=self.user, has_read=False)

        uuids = [notification1.uuid, notification2.uuid]
        mark_read(self.user, uuids)

        notification1.refresh_from_db()
        notification2.refresh_from_db()

        assert notification1.has_read is True
        assert notification2.has_read is True

    def test_mark_read_does_not_affect_other_users_notifications(self):
        # Create notifications for this test
        notification1 = NotificationFactory(recipient=self.user, has_read=False)
        notification2 = NotificationFactory(recipient=self.user, has_read=False)
        notification3 = NotificationFactory(
            recipient=self.other_user,
            has_read=False,
        )

        uuids = [notification1.uuid, notification2.uuid]
        mark_read(self.user, uuids)

        notification3.refresh_from_db()

        assert notification3.has_read is False

    def test_mark_read_with_no_unread_notifications(self):
        # Create notifications for this test
        notification1 = NotificationFactory(recipient=self.user, has_read=True)
        notification2 = NotificationFactory(recipient=self.user, has_read=True)

        uuids = [notification1.uuid, notification2.uuid]
        mark_read(self.user, uuids)

        notification1.refresh_from_db()
        notification2.refresh_from_db()

        assert notification1.has_read is True
        assert notification2.has_read is True
