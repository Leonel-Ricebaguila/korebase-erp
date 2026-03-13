from .models import Notification

def notify(user, message, notification_type='info', link=None):
    """
    Utility function to create a new notification for a specific user.
    """
    if user and user.is_authenticated:
        Notification.objects.create(
            user=user,
            message=message,
            notification_type=notification_type,
            link=link
        )
