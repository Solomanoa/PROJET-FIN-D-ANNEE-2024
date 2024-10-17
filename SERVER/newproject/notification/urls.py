from django.urls import path
from .views import create_notification, update_notification, delete_notification

urlpatterns = [
    path('notifications/', create_notification, name='create_notification'),
    path('notifications/<int:notification_id>/', update_notification, name='update_notification'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
]
