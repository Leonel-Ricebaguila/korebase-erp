from .models import Notification

def notifications_processor(request):
    """
    Context processor to make the unread notification count
    globally available across all templates.
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
