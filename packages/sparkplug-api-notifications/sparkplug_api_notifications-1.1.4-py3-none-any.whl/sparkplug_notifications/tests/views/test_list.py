from apps.users.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sparkplug_notifications.factories import NotificationFactory

from ..utils import create_partition_for_today


class TestListView(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.client = APIClient()
        self.user = UserFactory()
        self.other_user = UserFactory()

        # Create notifications for testing
        self.notification1 = NotificationFactory(
            recipient=self.user,
            is_starred=True,
            has_read=False,
        )
        self.notification2 = NotificationFactory(
            recipient=self.user,
            is_starred=False,
            has_read=True,
        )
        self.notification3 = NotificationFactory(
            recipient=self.other_user,
            is_starred=True,
            has_read=False,
        )

        self.url = reverse("sparkplug_notifications:list")

    def test_list_view_returns_notifications_for_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        uuids = [n["uuid"] for n in response.data["results"]]
        assert self.notification1.uuid in uuids
        assert self.notification2.uuid in uuids

    def test_list_view_filters_is_starred_notifications(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"is_starred": "true"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        uuids = [n["uuid"] for n in response.data["results"]]
        assert self.notification1.uuid in uuids

    def test_list_view_excludes_other_users_notifications(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        uuids = [n["uuid"] for n in response.data["results"]]
        assert self.notification3.uuid in uuids
