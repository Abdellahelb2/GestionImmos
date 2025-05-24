from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.recipient,
            message=f"Vous avez reçu un nouveau message de {instance.sender.username} concernant {instance.bien.name}"
        )
