from apps.users.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sparkplug_notifications.factories import NotificationFactory

from ..utils import create_partition_for_today


class TestMarkReadView(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.client = APIClient()
        self.user = UserFactory()
        self.other_user = UserFactory()

        self.url = reverse("sparkplug_notifications:mark_read")

        # Create notifications for testing
        self.notification1 = NotificationFactory(
            recipient=self.user, has_read=False
        )
        self.notification2 = NotificationFactory(
            recipient=self.user, has_read=False
        )
        self.notification3 = NotificationFactory(
            recipient=self.other_user, has_read=False
        )

    def test_mark_read_marks_notifications_as_read(self):
        uuids = [self.notification1.uuid, self.notification2.uuid]
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"uuids": uuids},
            format="json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        self.notification3.refresh_from_db()

        assert self.notification1.has_read is True
        assert self.notification2.has_read is True
        assert self.notification3.has_read is False

    def test_mark_read_does_not_affect_other_users_notifications(self):
        uuids = [self.notification1.uuid]
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"uuids": uuids},
            format="json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.notification1.refresh_from_db()
        self.notification3.refresh_from_db()

        assert self.notification1.has_read is True
        assert self.notification3.has_read is False

    def test_mark_read_requires_authentication(self):
        uuids = [self.notification1.uuid]
        response = self.client.patch(
            self.url,
            {"uuids": uuids},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_mark_read_with_empty_uuids(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"uuids": []},
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        assert self.notification1.has_read is False
        assert self.notification2.has_read is False

    def test_mark_read_with_invalid_uuid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"uuids": ["not-a-real-uuid"]},
            format="json",
        )
        # Should still return 204, but nothing is marked as read
        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        assert self.notification1.has_read is False
        assert self.notification2.has_read is False

    def test_mark_read_only_marks_owned_notifications(self):
        uuids = [self.notification1.uuid, self.notification3.uuid]
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"uuids": uuids},
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        self.notification3.refresh_from_db()

        assert self.notification1.has_read is True
        assert self.notification2.has_read is False
        assert self.notification3.has_read is False
