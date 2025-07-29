from datetime import timedelta

from django.db import connection
from django.utils.timezone import now


def create_partition_for_today():
    """
    Create a partition for the current date in the Notification table.
    """
    today = now().date()
    next_day = today + timedelta(days=1)
    partition_name = (
        f"sparkplug_notifications_notification_p{today.strftime('%Y%m%d')}"
    )

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {partition_name}
            PARTITION OF sparkplug_notifications_notification
            FOR VALUES FROM ('{today}') TO ('{next_day}');
            """
        )
