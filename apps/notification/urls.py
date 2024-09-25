from django.urls import path

from .views import notification_list_view, notification_retrieve_view

urlpatterns = [
    path("", notification_list_view, name="notification-list"),
    path("<int:pk>", notification_retrieve_view, name="notification-retrieve"),
]
