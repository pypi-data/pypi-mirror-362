import factory
from apps.users.factories import UserFactory

from sparkplug_notifications.models.notification import Notification


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    recipient = factory.SubFactory(UserFactory)
    actor = factory.SubFactory(UserFactory)
    actor_text = factory.Faker("name")
    message = factory.Faker("sentence")
    has_read = False
    is_starred = False
    target_route = factory.Dict({"url": "/example"})
