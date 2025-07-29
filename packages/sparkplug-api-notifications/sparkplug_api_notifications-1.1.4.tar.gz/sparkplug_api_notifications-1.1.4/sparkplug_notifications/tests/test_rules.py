from apps.users.factories import UserFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from freezegun import freeze_time

from sparkplug_notifications.factories import NotificationFactory
from sparkplug_notifications.rules import is_recipient

from .utils import create_partition_for_today


@freeze_time("2025-03-31")
class TestNotificationRules(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.user = UserFactory()
        self.other_user = UserFactory()
        self.notification = NotificationFactory(recipient=self.user)

    def test_is_recipient_true(self):
        # User is the recipient of the notification
        assert is_recipient(self.notification, self.user) is True

    def test_is_recipient_false(self):
        # User is not the recipient of the notification
        assert is_recipient(self.notification, self.other_user) is False

    def test_is_recipient_anonymous_user(self):
        # Use Django's built-in AnonymousUser
        anonymous_user = AnonymousUser()
        assert is_recipient(self.notification, anonymous_user) is False
