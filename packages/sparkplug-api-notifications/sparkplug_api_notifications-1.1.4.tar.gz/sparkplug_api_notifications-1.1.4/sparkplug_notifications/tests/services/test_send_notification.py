from unittest.mock import patch

from apps.users.factories import UserFactory
from django.test import TestCase
from freezegun import freeze_time

from sparkplug_notifications.models import Notification
from sparkplug_notifications.services import send_notification

from ..utils import create_partition_for_today


@freeze_time("2025-03-31")
class TestSendNotification(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.user = UserFactory(uuid="recipient-uuid")
        self.actor = UserFactory(uuid="actor-uuid")

    @patch(
        "sparkplug_notifications.services.send_notification.send_client_action"
    )
    def test_send_notification_creates_notification(
        self, mock_send_client_action
    ):
        send_notification(
            recipient_uuid=self.user.uuid,
            actor_uuid=self.actor.uuid,
            message="Test message",
            target_route={"url": "/test"},
        )

        notification = Notification.objects.filter(
            recipient_id=self.user.id,
            actor=self.actor,
            message="Test message",
        ).first()

        assert notification is not None
        assert notification.target_route == {"url": "/test"}
        mock_send_client_action.assert_called_once()
