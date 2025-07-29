from apps.users.factories import UserFactory
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sparkplug_notifications.factories import NotificationFactory

from ..utils import create_partition_for_today


class TestUnreadCountView(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.client = APIClient()
        self.user = UserFactory()
        self.other_user = UserFactory()

        # Create notifications for testing
        NotificationFactory(recipient=self.user, has_read=False)
        NotificationFactory(recipient=self.user, has_read=True)
        NotificationFactory(recipient=self.other_user, has_read=False)

        self.url = reverse("sparkplug_notifications:unread_count")

    def test_unread_count_view_returns_correct_count(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == 1  # One unread notification for self.user

    def test_unread_count_view_returns_zero_for_no_notifications(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == 0  # No notifications for new_user
