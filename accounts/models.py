from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('manager', 'Project Manager'),
        ('team_lead', 'Team Lead'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('tester', 'QA Tester'),
        ('stakeholder', 'Stakeholder'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    @property
    def get_notification_settings(self):
        try:
            return self.notification_settings
        except NotificationSettings.DoesNotExist:
            return NotificationSettings.objects.create(user=self)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    years_of_experience = models.PositiveIntegerField(default=0)
    preferred_working_hours = models.JSONField(default=dict)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    notification_frequency = models.CharField(
        max_length=20,
        choices=[
            ('real_time', 'Real-time'),
            ('daily', 'Daily digest'),
            ('weekly', 'Weekly digest')
        ],
        default='real_time'
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='led_teams')
    members = models.ManyToManyField(CustomUser, related_name='teams')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)  # e.g., 'login', 'profile_update', 'project_created'
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
    
    
    
##############################


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class NotificationSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_settings')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Notification Settings"

@receiver(post_save, sender=CustomUser)
def create_or_update_notification_settings(sender, instance, created, **kwargs):
    NotificationSettings.objects.get_or_create(user=instance)   