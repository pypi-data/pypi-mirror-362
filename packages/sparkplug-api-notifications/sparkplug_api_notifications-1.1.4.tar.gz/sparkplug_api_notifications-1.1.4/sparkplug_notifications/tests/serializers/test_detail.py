from unittest.mock import Mock

from sparkplug_notifications.serializers.detail import DetailSerializer


class TestDetailSerializer:
    def test_get_actor_uuid_with_actor(self):
        # Mock a Notification object with an actor that has a UUID
        mock_actor = Mock(uuid="123e4567-e89b-12d3-a456-426614174000")
        mock_notification = Mock(actor=mock_actor)

        serializer = DetailSerializer()

        # Call the get_actor_uuid method
        result = serializer.get_actor_uuid(mock_notification)

        assert result == "123e4567-e89b-12d3-a456-426614174000"

    def test_get_actor_uuid_without_actor(self):
        # Mock a Notification object with no actor
        mock_notification = Mock(actor=None)

        serializer = DetailSerializer()

        # Call the get_actor_uuid method
        result = serializer.get_actor_uuid(mock_notification)

        assert result is None
