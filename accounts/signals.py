from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import NotificationSettings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_notification_settings(sender, instance, created, **kwargs):
    if created:
        NotificationSettings.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_notification_settings(sender, instance, **kwargs):
    try:
        instance.notification_settings.save()
    except NotificationSettings.DoesNotExist:
        NotificationSettings.objects.create(user=instance)
        
        
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import NotificationSettings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_notification_settings(sender, instance, created, **kwargs):
    if created:
        NotificationSettings.objects.get_or_create(user=instance)
    else:
        try:
            instance.notification_settings.save()
        except NotificationSettings.DoesNotExist:
            NotificationSettings.objects.create(user=instance)        