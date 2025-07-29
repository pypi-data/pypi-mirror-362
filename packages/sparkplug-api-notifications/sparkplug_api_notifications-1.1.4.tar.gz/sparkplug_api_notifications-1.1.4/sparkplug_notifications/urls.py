from django.urls import path

from . import views

app_name = "sparkplug_notifications"

urlpatterns = [
    path(
        "mark-read/",
        views.MarkReadView.as_view(),
        name="mark_read",
    ),
    path(
        "<str:uuid>/set-star/",
        views.SetStarView.as_view(),
        name="set_star",
    ),
    path(
        "unread-count/",
        views.UnreadCountView.as_view(),
        name="unread_count",
    ),
    path(
        "",
        views.ListView.as_view(),
        name="list",
    ),
]
