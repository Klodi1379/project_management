# projects/management/commands/check_deadlines.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from projects.models import Task, Notification

class Command(BaseCommand):
    help = 'Check for approaching deadlines and create notifications'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        approaching_tasks = Task.objects.filter(
            due_date__range=[today, today + timedelta(days=3)],
            status__in=['not_started', 'in_progress']
        )

        for task in approaching_tasks:
            Notification.objects.create(
                user=task.assigned_to,
                notification_type='deadline',
                task=task,
                message=f"Task '{task.name}' in project '{task.project.name}' is due soon."
            )

        self.stdout.write(self.style.SUCCESS('Successfully checked for approaching deadlines'))
