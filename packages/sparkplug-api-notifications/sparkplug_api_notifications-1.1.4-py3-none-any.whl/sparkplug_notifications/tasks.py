from typing import Any

from huey.contrib.djhuey import db_task

from . import services


@db_task()
def send_notification(  # noqa: PLR0913
    *,
    recipient_uuid: str,
    message: str,
    actor_uuid: str | None = None,
    actor_text: str = "",
    target_route: Any = None,  # noqa: ANN401
    target_actor: bool = False,
) -> None:
    services.send_notification(
        recipient_uuid=recipient_uuid,
        message=message,
        actor_uuid=actor_uuid,
        actor_text=actor_text,
        target_route=target_route,
        target_actor=target_actor,
    )
