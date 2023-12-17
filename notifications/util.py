from django.contrib.auth import get_user_model
from .models import Notification
from django.utils import timezone
def send_credit_notification(user, credits_added):
    content = f"{credits_added} credits have been added to your account."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )
