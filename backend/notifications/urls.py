from django.urls import path

from .views import (
    fetch_all_notifications,
    fetch_unread_notifications,
    mark_all_notifications_as_read,
)

app_name = "notifications"

urlpatterns = [
    path("all/", fetch_all_notifications, name="list"),
    path("unread/", fetch_unread_notifications, name="unread"),
    path("mark/", mark_all_notifications_as_read, name="mark"),
]
