from apps.users.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sparkplug_notifications.factories import NotificationFactory

from ..utils import create_partition_for_today


class TestSetStarView(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.client = APIClient()
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.notification = NotificationFactory(
            recipient=self.user,
            is_starred=False,
        )

    def test_set_star_view_updates_is_starred_field(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "sparkplug_notifications:set_star",
            kwargs={"uuid": self.notification.uuid},
        )
        response = self.client.patch(
            url,
            data={"is_starred": True},
            format="json",
        )
        self.notification.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.notification.is_starred is True

    def test_set_star_view_fails_for_unauthorized_user(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse(
            "sparkplug_notifications:set_star",
            kwargs={"uuid": self.notification.uuid},
        )
        response = self.client.patch(
            url,
            data={"is_starred": True},
            format="json",
        )
        self.notification.refresh_from_db()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.notification.is_starred is False

    def test_set_star_view_fails_for_invalid_data(self):
        self.client.force_authenticate(user=self.user)

        url = reverse(
            "sparkplug_notifications:set_star",
            kwargs={"uuid": self.notification.uuid},
        )
        response = self.client.patch(
            url,
            data={"is_starred": "invalid_value"},
            format="json",
        )
        self.notification.refresh_from_db()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.notification.is_starred is False
